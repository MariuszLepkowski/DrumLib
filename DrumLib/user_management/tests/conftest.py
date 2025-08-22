import pytest
from django.contrib.auth.models import User
from user_management_app.models import Profile


@pytest.fixture
def user():
    """
    Fixture creating a new User object.
    """
    return User.objects.create_user(
        username="testuser",
        password="password123",
        first_name="John",
        last_name="Doe",
        email="testuser@example.com",
    )


@pytest.fixture
def profile(user):
    """
    Fixture that retrieves the profile associated with the user.
    It is assumed that the profile is automatically created by a signal.
    """
    return Profile.objects.get(user=user)
