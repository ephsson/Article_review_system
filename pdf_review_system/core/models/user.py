# core/models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("editor", "Editor"),
        ("judge", "Judge"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    interests = models.TextField(blank=True, null=True)  # CSV formatlı keyword listesi
    interest_vector = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
