from django.db import models


class Album(models.Model):
    """
    Model representing a music album.

    Attributes:
    - title: Album title.
    - artists: Many-to-many relationship with Artist model, indicating the artists or bands associated with the album.
    - release_year: Year of album release.
    - genre: Music genre of the album.
    - drummers: Many-to-many relationship with Drummer model, stores drummers associated with the album.
    - tracks: Many-to-many relationship with Track model, stores tracks included in the album.
    - album_url: album_url.
    - album_cover: Cover image of the album.
    """

    title = models.CharField(max_length=255)
    artists = models.ManyToManyField(
        "Artist", related_name="albums_featured", blank=True
    )
    release_year = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    drummers = models.ManyToManyField(
        "drummers.Drummer", related_name="albums_played", blank=True
    )
    tracks = models.ManyToManyField("Track", related_name="albums", blank=True)
    album_url = models.TextField(blank=True, null=True)
    album_cover = models.ImageField(upload_to="album_covers/", blank=False, null=False)

    def __str__(self):
        return self.title


class Artist(models.Model):
    """
    Model representing a music artist.

    Attributes:
    - name: Artist name.
    - collaborating_drummers: Many-to-many relationship with Drummer model, stores drummers collaborating with the artist.
    """

    name = models.CharField(max_length=255, unique=True)
    collaborating_drummers = models.ManyToManyField(
        "drummers.Drummer",
        related_name="artists_collaborating_with_drummer",
        blank=True,
    )

    def __str__(self):
        return self.name


class Track(models.Model):
    """
    Model representing a music track.

    Attributes:
    - title: Track title.
    - artist: Many-to-many relationship with Artist model, indicating artists or bands associated with the track.
    - drummers: Many-to-many relationship with Drummer model, stores drummers associated with the track.
    - track_url: track URL.
    """

    title = models.CharField(max_length=255)
    artists = models.ManyToManyField(
        "Artist", related_name="tracks_with_artist", blank=True
    )
    drummers = models.ManyToManyField(
        "drummers.Drummer", related_name="tracks_played", blank=True
    )
    track_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
