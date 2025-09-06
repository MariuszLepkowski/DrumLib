import pytest
from drummers.models import Drummer, DrummerPhoto


@pytest.mark.django_db
def test_drummer_photo_single_str():
    drummer = Drummer.objects.create(first_name="Vinnie", last_name="Colaiuta")
    photo = DrummerPhoto.objects.create()
    photo.drummers.add(drummer)
    assert str(photo) == f"Vinnie Colaiuta's Photo"


@pytest.mark.django_db
def test_drummer_photo_str_multiple_drummers():
    drummer1 = Drummer.objects.create(first_name="John", last_name="Bonham")
    drummer2 = Drummer.objects.create(first_name="Keith", last_name="Moon")
    photo = DrummerPhoto.objects.create()
    photo.drummers.add(drummer1, drummer2)
    assert str(photo) == "Photo with John Bonham, Keith Moon"
