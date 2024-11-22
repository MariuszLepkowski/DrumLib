import pytest
from django.contrib.auth.models import User
from user_management_app.models import Profile
from user_management_app.forms import UserProfileForm


@pytest.mark.django_db
class TestUserProfileForm:
    @pytest.mark.edit_user_profile
    def test_profile_initialization_with_user_data(self):
        # Arrange: Create a user with first_name and last_name
        user = User.objects.create_user(
            username="testuser",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        profile = Profile.objects.create(user=user)

        # Act: Initialize the form with the profile instance
        form = UserProfileForm(instance=profile)

        # Assert: Check if the initial values match the user's data
        assert form.fields['first_name'].initial == "John"
        assert form.fields['last_name'].initial == "Doe"

