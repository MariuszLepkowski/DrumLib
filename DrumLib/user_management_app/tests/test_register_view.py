import pytest
from user_management_app.views import register
from django.urls import reverse, resolve
from django.contrib.auth.models import User


@pytest.mark.registration_tests
@pytest.mark.django_db
class TestRegisterView:
    def test_register_view_get(self, client):
        """
        Test the register view with a GET request:
        - Checks if the URL resolves to the correct view.
        - Ensures a 200 response status.
        - Confirms the correct template and context are used.
        """
        url = reverse('user_management_app:register')
        response = client.get(url)

        # Check the resolved function (optional, integrates the removed test)
        assert resolve(url).func == register

        # Check response and template
        assert response.status_code == 200
        assert 'user_management_app/register.html' in [t.name for t in response.templates]

        # Check if the form is passed in the context
        assert 'form' in response.context

    def test_register_view_post_valid_data(self, client):
        """Test that valid POST data registers a new user and redirects to profile."""
        url = reverse('user_management_app:register')
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "new_user",
            "email": "newuser@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
        }
        response = client.post(url, data=valid_data)

        # Assert the user is created and logged in
        assert response.status_code == 302  # Redirect after success
        assert response.url == reverse('user_management_app:profile')
        assert User.objects.filter(username="new_user").exists()

    def test_register_view_post_invalid_data(self, client):
        """Test that invalid POST data does not register a new user."""
        url = reverse('user_management_app:register')
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "new_user",
            "email": "newuser@example.com",
            "password1": "securepassword123",
            "password2": "mismatchpassword123",  # Passwords don't match
        }
        response = client.post(url, data=invalid_data)

        # Assert no user is created and form is re-rendered with errors
        assert response.status_code == 200
        assert 'user_management_app/register.html' in [t.name for t in response.templates]
        assert not User.objects.filter(username="new_user").exists()
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_logged_in_user_sees_error_302_page(self, client, django_user_model):
        """Test that a logged-in user sees an error 302 page when trying to access register."""
        # Log in a user
        user = django_user_model.objects.create_user(username="testuser", password="password123")
        client.login(username="testuser", password="password123")

        url = reverse('user_management_app:register')
        response = client.get(url)

        # Assert status code 302 and correct template
        assert response.status_code == 302
        assert 'user_management_app/registration-error-302.html' in [t.name for t in response.templates]
        assert b"You are already logged in. You cannot access the registration page." in response.content
