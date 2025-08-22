from django.contrib.auth.models import User
from django.db import models


class DrummerSuggestion(models.Model):
    name = models.CharField(max_length=255)
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class AlbumSuggestion(models.Model):
    album_author = models.CharField(max_length=255)
    album_title = models.CharField(max_length=255)
    drummers_on_album = models.CharField(max_length=255)
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title
