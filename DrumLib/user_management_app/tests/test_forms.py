import pytest
from django.contrib.auth.models import User
from user_management_app.forms import UserRegistrationForm


class TestRegistration:

    @pytest.mark.registration_tests
    def test_user_registration_form(self):
        pass