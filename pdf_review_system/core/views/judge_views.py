from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from core.models import Submission, CustomUser, JudgeNote
import json

@csrf_exempt
def judge_list_submissions(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")

    if not username:
        return JsonResponse({"error": "Username is required"}, status=400)

    try:
        judge = CustomUser.objects.get(username=username, role="judge")
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Judge not found"}, status=404)

    submissions = Submission.objects.filter(assigned_judge=judge)

    submission_list = []
    for s in submissions:
        submission_list.append({
            "submission_id": s.submission_id,
            "status": s.status,
            "anonymized_pdf": request.build_absolute_uri(s.anonymized_pdf.url) if s.anonymized_pdf else None
        })

    return JsonResponse({"submissions": submission_list}, status=200)

def judge_view_submission(request, submission_id):
    return JsonResponse({"message": f"judge_view_submission placeholder for {submission_id}"})

@csrf_exempt
def judge_add_note(request, submission_id):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    note_text = data.get("note")

    if not username or not note_text:
        return JsonResponse({"error": "username and note are required"}, status=400)

    try:
        judge = CustomUser.objects.get(username=username, role="judge")
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Judge not found"}, status=404)

    try:
        submission = Submission.objects.get(submission_id=submission_id)
    except Submission.DoesNotExist:
        return JsonResponse({"error": "Submission not found"}, status=404)

    if submission.assigned_judge != judge:
        return JsonResponse({"error": "Judge not authorized for this submission"}, status=403)

    JudgeNote.objects.create(
        submission=submission,
        judge=judge,
        note=note_text
    )

    # Statüyü isteğe bağlı olarak güncelleyebilirsin
    if submission.status == "assigning":
        submission.status = "in_review"
        submission.save()

    return JsonResponse({"message": "Note saved successfully."}, status=201)
