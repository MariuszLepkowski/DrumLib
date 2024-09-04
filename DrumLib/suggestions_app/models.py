from django.db import models
from django.contrib.auth.models import User


class DrummerSuggestion(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class AlbumSuggestion(models.Model):
    title = models.CharField(max_length=255)
    drummer = models.ForeignKey('drummers_app.Drummer', on_delete=models.SET_NULL, null=True, blank=True)
    drummer_suggestion = models.ForeignKey(DrummerSuggestion, on_delete=models.SET_NULL, null=True, blank=True)
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
