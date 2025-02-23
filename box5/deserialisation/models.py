from django.db import models

class UserPreference(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    width = models.FloatField()
    height = models.FloatField()
    counrty = models.CharField(max_length=100)  # Note: Field name kept as "counrty" per requirements

    def __str__(self):
        return f"{self.name} ({self.age})"
