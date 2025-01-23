import pytest
from django.contrib.auth.models import User
from drummers_app.models import Drummer
from discography_app.models import Album


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def drummer():
    return Drummer.objects.create(name="John Bonham")


@pytest.fixture
def album():
    return Album.objects.create(title="Led Zeppelin IV", release_year=1971, genre="Rock")
