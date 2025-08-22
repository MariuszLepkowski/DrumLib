import pytest
from django.contrib.auth.models import User
from user_management_app.forms import UserRegistrationForm

test_data = [
    (  # valid_registration
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "test_user",
            "email": "testemail@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        },
        True,
    ),
    (  # invalid_passwords_mismatch
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "test_user",
            "email": "testemail@example.com",
            "password1": "testpassword123",
            "password2": "differentpassword123",
        },
        False,
    ),
    (  # missing_email
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "test_user",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        },
        False,
    ),
    (  # wrong mail format
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "test_user",
            "email": "mail.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        },
        False,
    ),
]


@pytest.mark.registration_tests
@pytest.mark.django_db
class TestRegistration:

    @pytest.mark.parametrize(
        "data, is_valid",
        test_data,
        ids=[
            "valid_registration",
            "invalid_passwords_mismatch",
            "missing_email",
            "wrong_mail_format",
        ],
    )
    def test_user_registration_form(self, data, is_valid):
        form = UserRegistrationForm(data=data)

        assert form.is_valid() == is_valid

        if form.is_valid():
            form.save()
            assert User.objects.filter(username="test_user").exists()
