import pytest
from drummers.models import Drummer, DrummerPhoto


@pytest.mark.django_db
def test_drummer_str():
    drummer = Drummer.objects.create(name="Vinnie Colaiuta")
    assert str(drummer) == "Vinnie Colaiuta"


@pytest.mark.django_db
def test_drummer_photo_relationship():
    # Create drummer objects
    drummer1 = Drummer.objects.create(name="Neil Peart")
    drummer2 = Drummer.objects.create(name="Ginger Baker")

    # Create two photo objects
    photo1 = DrummerPhoto.objects.create(image_author="John Doe")
    photo2 = DrummerPhoto.objects.create(image_author="Jane Doe")

    # Add drummers to both photos at once
    photo1.drummers.add(drummer1, drummer2)
    photo2.drummers.add(drummer1, drummer2)

    # Add photos to both drummers
    drummer1.photos.add(photo1, photo2)
    drummer2.photos.add(photo1, photo2)

    # Refresh objects to ensure the latest data is loaded from the database
    drummer1.refresh_from_db()
    drummer2.refresh_from_db()
    photo1.refresh_from_db()
    photo2.refresh_from_db()

    # Check the relationships for photo1
    assert drummer1 in photo1.drummers.all()
    assert drummer2 in photo1.drummers.all()
    assert photo1 in drummer1.photos.all()
    assert photo1 in drummer2.photos.all()

    # Check the relationships for photo2
    assert drummer1 in photo2.drummers.all()
    assert drummer2 in photo2.drummers.all()
    assert photo2 in drummer1.photos.all()
    assert photo2 in drummer2.photos.all()
