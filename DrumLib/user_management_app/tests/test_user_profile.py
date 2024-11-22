import pytest
from django.contrib.auth.models import User
from user_management_app.models import Profile
from user_management_app.forms import UserProfileForm


@pytest.mark.django_db
@pytest.mark.user_profile
class TestUserProfileForm:

    def test_profile_object_creation_signal(self):
        """
        Test whether the Profile is automatically created when a User is created.
        """
        # Act: Create a user
        user = User.objects.create_user(username="testuser", password="password123")

        # Assert: Check if a Profile object was automatically created
        assert Profile.objects.filter(user=user).exists()

    def test_profile_form_initialization_with_user_data(self):
        """
        Test that UserProfileForm initializes with user's first_name and last_name correctly.
        This ensures that the form pre-populates fields using the related User instance's data.
        """
        # Arrange: Create a user with first_name and last_name
        user = User.objects.create_user(
            username="testuser",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        profile = Profile.objects.get(user=user)  # Profile is created via signal

        # Act: Initialize the form with the profile instance
        form = UserProfileForm(instance=profile)

        # Assert: Verify the form's type and field initialization
        assert isinstance(form, UserProfileForm)
        assert form.fields['first_name'].initial == "John"
        assert form.fields['last_name'].initial == "Doe"
        assert profile.user == user  # Ensure profile is correctly linked to the user

    def test_profile_form_save_and_user_object_update(self):
        """
        Test saving the UserProfileForm updates both the Profile and User models.
        """
        # Arrange: Create a user and their profile
        user = User.objects.create_user(
            username="testuser",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        profile = Profile.objects.get(user=user)

        # Act: Update the form data and save it
        form_data = {
            "first_name": "Jane",  # Changing first_name
            "last_name": "Smith",  # Changing last_name
            "personal_info": "New personal info",  # Update profile's personal info
            "avatar": None,  # Avatar can be updated or left unchanged
        }
        form = UserProfileForm(instance=profile, data=form_data)

        # Assert: Check if the form is valid
        assert form.is_valid()

        # Save the form
        profile = form.save(commit=False)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()  # Save the User model
        profile.save()  # Save the Profile model

        # Refresh both Profile and User objects to ensure they reflect the latest data
        profile.refresh_from_db()
        user.refresh_from_db()

        # Assert: Check if the changes are reflected in the Profile model
        assert profile.personal_info == "New personal info"  # Check profile data update
        assert user.first_name == "Jane"  # Check if user's first name was updated
        assert user.last_name == "Smith"  # Check if user's last name was updated

    def test_profile_form_max_length_validation(self):
        # Arrange
        long_string = "a" * 31  # Assuming max_length=30
        form_data = {
            "first_name": long_string,
            "last_name": "Doe",
            "personal_info": "Some personal info",
            "avatar": None,
        }
        user = User.objects.create_user(username="testuser", password="password123")
        profile = Profile.objects.get(user=user)

        # Act
        form = UserProfileForm(instance=profile, data=form_data)

        # Assert
        assert not form.is_valid()
        assert "Ensure this value has at most" in form.errors['first_name'][0]
