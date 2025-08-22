import pytest
from drummers_app.models import Drummer, DrummerPhoto


@pytest.mark.django_db
def test_drummer_photo_single_str():
    drummer = Drummer.objects.create(name="Vinnie Colaiuta")
    photo = DrummerPhoto.objects.create()
    photo.drummers.add(drummer)
    assert str(photo) == f"Vinnie Colaiuta's Photo"


@pytest.mark.django_db
def test_drummer_photo_str_multiple_drummers():
    drummer1 = Drummer.objects.create(name="John Bonham")
    drummer2 = Drummer.objects.create(name="Keith Moon")
    photo = DrummerPhoto.objects.create()
    photo.drummers.add(drummer1, drummer2)
    assert str(photo) == "Photo with John Bonham, Keith Moon"
