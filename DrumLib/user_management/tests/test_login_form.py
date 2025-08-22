import pytest
from django.contrib.auth.models import User
from user_management.forms import CustomAuthenticationForm


@pytest.mark.login_tests
@pytest.mark.django_db
class TestCustomAuthenticationForm:

    @pytest.mark.parametrize(
        "username, password, expected_error",
        [
            ("existing_user", "correct_password", None),
            ("nonexistent_user", "any_password", "The user does not exist."),
            ("existing_user", "incorrect_password", "Invalid password. Try again."),
        ],
        ids=[
            "valid_login",
            "nonexistent_user",
            "incorrect_password",
        ],
    )
    def test_authentication_form(self, username, password, expected_error):
        User.objects.create_user(username="existing_user", password="correct_password")

        form_data = {"username": username, "password": password}

        form = CustomAuthenticationForm(data=form_data)

        if expected_error:
            assert not form.is_valid()
            assert expected_error in form.errors["__all__"][0]
        else:
            assert form.is_valid()
