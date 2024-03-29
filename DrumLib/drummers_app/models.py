from django.db import models


class Drummer(models.Model):
    """
    Model representing a drummer.

    Attributes:
    - name: Drummer's full name.
    - bio: Drummer's biography.
    - birth_date: Drummer's date of birth.
    - origin: Drummer's place of origin.
    - photos: Many-to-many relationship with DrummerPhoto model, stores drummer's photos.
    - collaborating_artists: Many-to-many relationship with Artist model, indicating artists the drummer has collaborated with.
    """
    name = models.CharField(max_length=255)
    bio = models.TextField()
    birth_date = models.DateField()
    origin = models.CharField(max_length=255)
    photos = models.ManyToManyField('DrummerPhoto', related_name='drummers_on_photo', blank=True)
    collaborating_artists = models.ManyToManyField('discography_app.Artist', blank=True)

    def __str__(self):
        return self.name


class DrummerPhoto(models.Model):
    """
    Model representing a photo of a drummer.

    Attributes:
    - drummers: Many-to-many relationship with Drummer model, indicating the drummers associated with the photo.
    - image: Binary representation of the drummer's photo.
    """
    drummers = models.ManyToManyField('Drummer')
    image = models.BinaryField()

    def __str__(self):
        drummer_names = ", ".join(drummer.name for drummer in self.drummers.all())
        if len(self.drummers.all()) > 1:
            return f"Photo with {drummer_names}"
        else:
            return f"{drummer_names}'s Photo"
