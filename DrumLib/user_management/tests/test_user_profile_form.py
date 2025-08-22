from io import BytesIO

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from user_management.forms import UserProfileForm
from user_management.models import Profile


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

    def test_profile_form_initialization_with_user_data(self, profile):
        """
        Test that UserProfileForm initializes with user's first_name and last_name correctly.
        This ensures that the form pre-populates fields using the related User instance's data.
        """

        # Act: Initialize the form with the profile instance
        form = UserProfileForm(instance=profile)

        # Assert: Verify the form's type and field initialization
        assert isinstance(form, UserProfileForm)
        assert form.fields["first_name"].initial == "John"
        assert form.fields["last_name"].initial == "Doe"
        assert (
            profile.user.username == "testuser"
        )  # Ensure profile is correctly linked to the user

    def test_profile_form_save_and_user_object_update(self, profile, user):
        """
        Test saving the UserProfileForm updates both the Profile and User models.
        """

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
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
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
        assert "Ensure this value has at most" in form.errors["first_name"][0]

    def test_profile_form_avatar_validation(self, profile, user):
        # Generate a valid image file
        image = Image.new("RGB", (100, 100), "white")
        image_file = BytesIO()
        image.save(image_file, format="JPEG")
        image_file.seek(0)  # Reset the file pointer to the beginning

        valid_image = SimpleUploadedFile(
            "avatar.jpg", image_file.read(), content_type="image/jpeg"
        )
        invalid_file = SimpleUploadedFile(
            "document.pdf", b"file_content", content_type="application/pdf"
        )

        # Test valid image
        form = UserProfileForm(
            instance=profile,
            data={
                "first_name": "John",
                "last_name": "Doe",
                "personal_info": "New personal info",
            },
            files={"avatar": valid_image},
        )
        assert form.is_valid()

        # Test invalid file
        form = UserProfileForm(
            instance=profile,
            data={
                "first_name": "John",
                "last_name": "Doe",
                "personal_info": "New personal info",
            },
            files={"avatar": invalid_file},
        )
        assert not form.is_valid(), "Form should be invalid with a non-image file."
        assert (
            "avatar" in form.errors
        ), "The error should be related to the avatar field."

    def test_profile_form_integrity_no_side_effects(self, profile, user):
        """
        Ensure that updating profile fields does not affect unrelated fields in the User model.
        """
        # Act: Update only profile fields
        form_data = {
            "personal_info": "Updated personal info",
        }
        form = UserProfileForm(instance=profile, data=form_data)

        assert form.is_valid(), f"Form errors: {form.errors}"
        profile = form.save(commit=False)
        profile.save()

        # Assert: Ensure unrelated User fields are unchanged
        user.refresh_from_db()
        assert user.username == "testuser", "Username should not be changed."
        assert user.email == "testuser@example.com", "Email should not be changed."
        assert user.first_name == "John", "First name should remain unchanged."
        assert user.last_name == "Doe", "Last name should remain unchanged."
