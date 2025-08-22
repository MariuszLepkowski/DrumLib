import pytest
from django.urls import resolve, reverse
from user_management.views import profile


@pytest.mark.django_db
class TestProfileView:
    def test_profile_view_accessible_for_logged_in_user(
        self, client, django_user_model
    ):
        """
        Test that the profile view is accessible for a logged-in user:
        - URL resolves to the correct view.
        - Response has a status code of 200.
        - The correct template is rendered.
        """
        # Arrange: Create and log in a user
        user = django_user_model.objects.create_user(
            username="testuser", password="password123"
        )
        client.login(username="testuser", password="password123")

        # Act: Send GET request to the profile view
        url = reverse("user_management:profile")
        response = client.get(url)

        # Assert: Check URL resolution, response status, and template
        assert resolve(url).func == profile
        assert response.status_code == 200
        assert "user_management/profile.html" in [t.name for t in response.templates]

    def test_profile_view_redirects_for_anonymous_user(self, client):
        """
        Test that the profile view redirects an anonymous user:
        - Response has a status code of 302.
        - The user is redirected to the login page with the 'next' parameter set.
        """
        # Act: Send GET request to the profile view without logging in
        url = reverse("user_management:profile")
        response = client.get(url)

        # Assert: Check redirection to the login page
        assert response.status_code == 302
        assert response.url == f"{reverse('user_management:login')}?next={url}"
