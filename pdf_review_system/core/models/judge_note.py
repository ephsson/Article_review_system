from django.db import models
from core.models import Submission, CustomUser

class JudgeNote(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    judge = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role": "judge"})
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.judge.username} on submission {self.submission.submission_id}"