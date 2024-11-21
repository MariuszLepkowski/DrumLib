import pytest
from django.contrib.auth.models import User
from user_management_app.models import Profile
from user_management_app.forms import UserProfileForm


@pytest.mark.django_db
class TestUserProfileForm:
    @pytest.mark.edit_user_profile
    def test_user_profile_form_initial_data(self):
        pass

    @pytest.mark.edit_user_profile
    def test_user_profile_form_valid_data(self):
        pass

    @pytest.mark.edit_user_profile
    def test_user_profile_form_invalid_data(self):
        pass