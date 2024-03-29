from django.db import models


class Album(models.Model):
    """
    Model representing a music album.

    Attributes:
    - title: Album title.
    - artist: Foreign key relationship with Artist model, indicating the artist or band associated with the album.
    - release_year: Year of album release.
    - genre: Music genre of the album.
    - drummers: Many-to-many relationship with Drummer model, stores drummers associated with the album.
    - tracks: Many-to-many relationship with Track model, stores tracks included in the album.
    """
    title = models.CharField(max_length=255)
    artist = models.ForeignKey('Artist', on_delete=models.SET_NULL, null=True, blank=True, related_name='albums')
    release_year = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    drummers = models.ManyToManyField('drummers_app.Drummer', related_name='albums_played', blank=True)
    tracks = models.ManyToManyField('discography_app.Track', related_name='albums', blank=True)

    def __str__(self):
        return self.title


class Artist(models.Model):
    """
    Model representing a music artist.

    Attributes:
    - name: Artist name.
    - collaborating_drummers: Many-to-many relationship with Drummer model, stores drummers collaborating with the artist.
    """
    name = models.CharField(max_length=255)
    collaborating_drummers = models.ManyToManyField("drummers_app.Drummer", blank=True)

    def __str__(self):
        return self.name


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
    drummers = models.ManyToManyField("drummers_app.Drummer", related_name='tracks_played', blank=True)

    def __str__(self):
        return self.title

