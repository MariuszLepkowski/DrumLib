import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password123')


@pytest.fixture
def another_user(db):
    return User.objects.create_user(username='anotheruser', password='password456')
