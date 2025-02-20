import pytest
from django.contrib.auth.models import User
from drummers_app.models import Drummer
from discography_app.models import Album


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")

@pytest.fixture
def another_user(db):
    return User.objects.create_user(username="another_user", email="another_user@example.com", password="password123")

@pytest.fixture
def staff_user():
    return User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)


@pytest.fixture
def drummer():
    return Drummer.objects.create(name="John Bonham")


@pytest.fixture
def album():
    return Album.objects.create(title="Led Zeppelin IV", release_year=1971, genre="Rock")
