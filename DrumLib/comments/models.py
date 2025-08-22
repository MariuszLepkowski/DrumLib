from discography_app.models import Album, Track
from django.contrib.auth.models import User
from django.db import models
from drummers_app.models import Drummer


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    drummer = models.ForeignKey(
        Drummer, on_delete=models.CASCADE, null=True, blank=True
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.created_at}: {self.text}"
