from django.contrib.auth.models import User
from django.db import models

# UserProfile extends the default Django User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('normal', 'Normal')])

    def __str__(self):
        return f'{self.user.username} ({self.role})'
