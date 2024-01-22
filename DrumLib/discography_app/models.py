from django.db import models
from drummers_app.models import Drummer


class Track(models.Model):
    """
    Model representing a music track.

    Attributes:
    - title: Track title.
    - artist: Foreign key relationship with Artist model, indicating the artist or band associated with the track.
    - drummers: Many-to-many relationship with Drummer model, stores drummers associated with the track.
    """
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    drummers = models.ManyToManyField(Drummer, related_name='tracks_played', blank=True)

    def __str__(self):
        return self.title
