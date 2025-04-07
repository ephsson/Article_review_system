from django.db import models

class Submission(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("assigning", "Referee Assignment In Progress"),
        ("in_review", "In Review"),
        ("reviewed", "Review Concluded"),
        ("published", "Published"),
        ("revisions_required", "Revisions Required"),
    ]

    submission_id = models.AutoField(primary_key=True)
    writer_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    authors = models.TextField(blank=True, null=True)        
    organizations = models.TextField(blank=True, null=True)  
    review_notes = models.TextField(blank=True, null=True)
    fasttext_vector = models.JSONField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='uploads/originals/')
    anonymized_pdf = models.FileField(upload_to='uploads/anonymized/', blank=True, null=True)
    assigned_judge = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'judge'},
        related_name='assigned_submissions'
    )

    def __str__(self):
        return f"Submission {self.submission_id} - {self.status}"
