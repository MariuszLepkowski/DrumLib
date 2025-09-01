from django.db import models


class Drummer(models.Model):
    """
    Model representing a drummer.

    Attributes:
    - name: Drummer's full name.
    - bio: Drummer's biography (optional).
    - birth_date: Drummer's date of birth (optional).
    - death_date: Drummer's date of death (optional, can be null if still alive or date of death is unknown).
    - nationality: Drummer's nationality (optional).
    - photos: Many-to-many relationship with DrummerPhoto model, stores drummer's photos (optional).
    - collaborating_artists: Many-to-many relationship with Artist model, indicating artists the drummer has collaborated with (optional).
    """

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    photos = models.ManyToManyField(
        "DrummerPhoto", related_name="drummers_on_photo", blank=True
    )
    collaborating_artists = models.ManyToManyField(
        "discography.Artist",
        related_name="drummers_collaborating_with_artist",
        blank=True,
    )

    @property
    def name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or ""

    def __str__(self):
        return self.name


class DrummerPhoto(models.Model):
    """
    Model representing a photo of a drummer.

    Attributes:
    - drummers: Many-to-many relationship with Drummer model, indicating the drummers associated with the photo.
    - image: Binary representation of the drummer's photo.
    - source: Field indicating the source of the photo.
    - image_author: Field indicating the author of the photo.
    """

    drummers = models.ManyToManyField(
        "Drummer", related_name="photos_of_drummer", blank=True
    )
    image = models.ImageField(upload_to="drummer_photos/", blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    image_author = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        drummer_names = ", ".join(drummer.name for drummer in self.drummers.all())
        if len(self.drummers.all()) > 1:
            return f"Photo with {drummer_names}"
        else:
            return f"{drummer_names}'s Photo"
