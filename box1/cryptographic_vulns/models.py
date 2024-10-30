# cryptographic_vulns/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='crypto_profile')
    role = models.CharField(max_length=50, choices=[('normal', 'Normal User'), ('admin', 'Admin User')])
    flag = models.CharField(max_length=100, null=True, blank=True)  # Admin user gets the flag

    def __str__(self):
        return self.user.username
