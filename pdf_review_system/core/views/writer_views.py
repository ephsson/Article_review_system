from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from core.models import Submission, JudgeNote
from core.services.anonymizer import anonymize_pdf
from core.services.keyword_extractor import (
    extract_entities_from_pdf,
    extract_keywords_from_pdf,
)
from core.services.vectorizer import vectorize_text
import os


@csrf_exempt
def writer_upload_submission(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)

    pdf_file = request.FILES.get("pdf_file")
    writer_email = request.POST.get("writer_email")

    if not pdf_file or not writer_email:
        return JsonResponse({"error": "Missing file or email"}, status=400)

    # 1. Submission nesnesini oluştur
    submission = Submission.objects.create(
        writer_email=writer_email,
        pdf_file=pdf_file,
        status="submitted"
    )

    original_path = os.path.join(settings.MEDIA_ROOT, submission.pdf_file.name)

    # 2. Authors ve organizations
    authors, orgs = extract_entities_from_pdf(original_path)
    submission.authors = authors
    submission.organizations = orgs

    # 3. Keywords → vektör
    keywords = extract_keywords_from_pdf(original_path)
    if keywords:
        submission.fasttext_vector = vectorize_text(" ".join(keywords))
    else:
        print("⚠️ No keywords extracted; fasttext_vector left empty.")

    # 4. Anonimleştirme işlemleri
    base_name = os.path.splitext(os.path.basename(submission.pdf_file.name))[0]
    anonymized_name = f"{base_name}_anonymized.pdf"
    anonymized_dir = os.path.join(settings.MEDIA_ROOT, "uploads/anonymized")
    anonymized_path = os.path.join(anonymized_dir, anonymized_name)

    os.makedirs(anonymized_dir, exist_ok=True)
    anonymize_pdf(original_path, anonymized_path)

    submission.anonymized_pdf.name = f"uploads/anonymized/{anonymized_name}"
    submission.save()

    return JsonResponse({
        "message": "Submission received and anonymized successfully.",
        "submission_id": submission.submission_id,
        "status": submission.status
    }, status=201)


@csrf_exempt
def writer_check_status(request, submission_id):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)

    writer_email = request.GET.get("email")
    if not writer_email:
        return JsonResponse({"error": "Email is required"}, status=400)

    try:
        submission = Submission.objects.get(submission_id=submission_id, writer_email=writer_email)
    except Submission.DoesNotExist:
        return JsonResponse({"error": "No matching submission found"}, status=404)

    response = {
        "submission_id": submission.submission_id,
        "status": submission.status
    }

    if submission.status in ["published", "revisions_required"]:
        notes = JudgeNote.objects.filter(submission=submission)
        response["judge_notes"] = [n.note for n in notes]

    return JsonResponse(response, status=200)
