from django.http import JsonResponse
from core.models import Submission

def public_list_published_submissions(request):
    published = Submission.objects.filter(status="published")

    result = []
    for s in published:
        result.append({
            "submission_id": s.submission_id,
            "title": f"Submission {s.submission_id}",
            "pdf_url": request.build_absolute_uri(s.pdf_file.url)
        })

    return JsonResponse({"published_submissions": result}, status=200)
