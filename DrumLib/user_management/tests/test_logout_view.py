import pytest
from user_management_app.views import logout_view
from django.contrib.auth.models import User
from django.urls import reverse, resolve


@pytest.mark.logout_tests
@pytest.mark.django_db
class TestLogoutView:
    def test_logout_view_url(self):
        path = reverse('user_management_app:logout')
        assert resolve(path).func == logout_view

    def test_user_logout(self, client):
        """
        Test that a logged-in user is successfully logged out.
        """
        # Arrange: Create and log in a user
        user = User.objects.create_user(username="testuser", password="password123")
        client.login(username="testuser", password="password123")

        # Ensure the user is logged in before the logout test
        response = client.get(reverse('user_management_app:logout'))
        assert response.status_code == 302  # Expect redirect after logout

        # Act: Check the session is cleared
        response = client.get(reverse('user_management_app:profile'))
        assert response.status_code == 302  # Redirect to login page (unauthorized)

    def test_logout_redirects_to_home(self, client):
        """
        Test that the logout redirects to the expected page.
        """
        # Arrange: Log in user
        user = User.objects.create_user(username="testuser", password="password123")
        client.login(username="testuser", password="password123")

        # Act: Perform logout
        response = client.get(reverse('user_management_app:logout'))

        # Assert: Check if redirected to the home page
        assert response.status_code == 302
        assert response.url == reverse("home_app:home_page")  # Assumes redirect to 'home'

    def test_logout_clears_session(self, client):
        """
        Test that the user's session is cleared after logout.
        """
        # Arrange: Log in the user
        user = User.objects.create_user(username="testuser", password="password123")
        client.login(username="testuser", password="password123")

        # Verify the user is authenticated
        assert client.session.get("_auth_user_id") == str(user.id)

        # Act: Log out
        client.get(reverse('user_management_app:logout'))

        # Assert: Ensure the session is cleared
        assert "_auth_user_id" not in client.session