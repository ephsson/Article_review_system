from django.http import JsonResponse
from core.models import Submission, CustomUser, JudgeNote
from core.services.vectorizer import vectorize_text
from django.views.decorators.csrf import csrf_exempt
import json
from numpy import dot
from numpy.linalg import norm

def compute_similarity(vec1, vec2):
    if not vec1 or not vec2:
        return 0.0
    return float(dot(vec1, vec2) / (norm(vec1) * norm(vec2) + 1e-8))

@csrf_exempt
def editor_suggest_judges(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        submission_id = data.get("submission_id")
        submission = Submission.objects.get(submission_id=submission_id)
    except (Submission.DoesNotExist, ValueError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid or missing submission ID"}, status=400)

    if not submission.fasttext_vector:
        return JsonResponse({"error": "Submission vector missing"}, status=400)

    judges = CustomUser.objects.filter(role="judge")
    scored_judges = []

    for judge in judges:
        if not judge.interest_vector:
            continue

        score = compute_similarity(submission.fasttext_vector, judge.interest_vector)
        scored_judges.append({
            "username": judge.username,
            "interests": judge.interests,
            "score": round(score, 4)
        })

    top_5 = sorted(scored_judges, key=lambda j: j["score"], reverse=True)[:5]

    return JsonResponse({
        "submission_id": submission_id,
        "judges": top_5
    }, status=200)



@csrf_exempt
def editor_add_judge(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)

    data = json.loads(request.body)

    username = data.get("username")
    interests = data.get("interests_csv")

    if not username or not interests:
        return JsonResponse({"error": "username and interests_csv are required"}, status=400)

    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    # Vektörleştirme
    interest_vector = vectorize_text(interests)

    judge = CustomUser.objects.create(
        username=username,
        role="judge",
        interests=interests,
        interest_vector=interest_vector
    )

    return JsonResponse({
        "message": "Judge created successfully",
        "id": judge.id,
        "username": judge.username,
        "interests": judge.interests,
        "vector": judge.interest_vector
    }, status=201)

@csrf_exempt
def editor_list_submissions(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests allowed"}, status=405)

    submissions = Submission.objects.all()

    submission_list = []
    for s in submissions:
        submission_list.append({
            "submission_id": s.submission_id,
            "writer_email": s.writer_email,
            "status": s.status,
            "authors": s.authors,
            "organizations": s.organizations,
            "assigned_judge": s.assigned_judge.username if s.assigned_judge else None
        })

    return JsonResponse({"submissions": submission_list}, status=200)

@csrf_exempt

def editor_assign_judge(request, submission_id):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    import json
    data = json.loads(request.body)

    judge_username = data.get("judge_username")
    if not judge_username:
        return JsonResponse({"error": "judge_username is required"}, status=400)

    # Hakem kullanıcıyı bul
    try:
        judge = CustomUser.objects.get(username=judge_username, role="judge")
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Judge not found"}, status=404)

    # Submission'ı bul
    try:
        submission = Submission.objects.get(submission_id=submission_id)
    except Submission.DoesNotExist:
        return JsonResponse({"error": "Submission not found"}, status=404)

    # Zaten atanmışsa uyarı verebiliriz
    if submission.assigned_judge:
        return JsonResponse({"error": "Submission already has a judge assigned"}, status=400)

    # Atama işlemi
    submission.assigned_judge = judge
    submission.status = "assigning"  # İstersen "in_review" da yapabiliriz
    submission.save()

    return JsonResponse({
        "message": f"Judge '{judge.username}' assigned to submission {submission_id}.",
        "assigned_judge": judge.username,
        "submission_id": submission.submission_id,
        "new_status": submission.status
    }, status=200)

@csrf_exempt
def editor_update_status(request, submission_id):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    import json
    data = json.loads(request.body)
    new_status = data.get("new_status")

    if new_status not in ["published", "revisions_required"]:
        return JsonResponse({"error": "Invalid status"}, status=400)

    try:
        submission = Submission.objects.get(submission_id=submission_id)
    except Submission.DoesNotExist:
        return JsonResponse({"error": "Submission not found"}, status=404)

    submission.status = new_status
    submission.save()

    return JsonResponse({
        "message": f"Status updated to '{new_status}' for submission {submission_id}."
    }, status=200)

def editor_list_judges(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)

    judges = CustomUser.objects.filter(role="judge")

    judge_list = [
        {
            "username": j.username,
            "interests": j.interests
        } for j in judges
    ]

    return JsonResponse({"judges": judge_list}, status=200)

@csrf_exempt
def editor_fetch_reviews(request, submission_id):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)

    try:
        notes = JudgeNote.objects.filter(submission__submission_id=submission_id)
        note_list = [n.note for n in notes]
    except:
        return JsonResponse({"error": "Submission not found"}, status=404)

    return JsonResponse({"judge_notes": note_list}, status=200)
