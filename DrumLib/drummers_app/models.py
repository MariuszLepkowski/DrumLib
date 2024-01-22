from django.db import models
from discography_app.models import Artist


class Drummer(models.Model):
    """
    Model representing a drummer.

    Attributes:
    - name: Drummer's full name.
    - bio: Drummer's biography.
    - year_of_birth: Year of drummer's birth.
    - year_of_death: Year of drummer's death (optional, can be null if still alive or year of death is unknown).
    - origin: Drummer's place of origin.
    - photos: Many-to-many relationship with DrummerPhoto model, stores drummer's photos.
    - collaborating_artists: Many-to-many relationship with Artist model, indicating artists the drummer has collaborated with.
    """
    name = models.CharField(max_length=255)
    bio = models.TextField()
    year_of_birth = models.IntegerField()
    year_of_death = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=255, blank=True, null=True)
    photos = models.ManyToManyField('DrummerPhoto', related_name='drummer', blank=True)
    collaborating_artists = models.ManyToManyField(Artist, related_name='collaborating_drummers', blank=True)

    def __str__(self):
        return self.name


class DrummerPhoto(models.Model):
    """
    Model representing a photo of a drummer.

    Attributes:
    - drummers: Many-to-many relationship with Drummer model, indicating the drummers associated with the photo.
    - image: Binary representation of the drummer's photo.

    """
    drummers = models.ManyToManyField(Drummer, related_name='photos')
    image = models.BinaryField()

    def __str__(self):
        drummer_names = ", ".join(drummer.name for drummer in self.drummers.all())

        if len(self.drummers.all()) > 1:
            return f"Photo with {drummer_names}"
        else:
            return f"{drummer_names}'s Photo"
