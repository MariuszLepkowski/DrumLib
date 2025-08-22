import pytest
from django.urls import resolve, reverse
from user_management_app.views import edit_profile


@pytest.fixture
def logged_in_user(client, django_user_model):
    """
    Fixture to create a user and log them in.
    """
    user = django_user_model.objects.create_user(
        username="testuser", password="password123"
    )
    client.login(username="testuser", password="password123")
    return user


@pytest.mark.user_profile
@pytest.mark.django_db
class TestEditProfileView:
    def test_edit_profile_view_resolves_to_correct_view(self):
        url = reverse("user_management_app:edit_profile")
        assert resolve(url).func == edit_profile

    def test_edit_profile_view_accessible_for_logged_in_user(
        self, client, logged_in_user
    ):
        url = reverse("user_management_app:edit_profile")
        response = client.get(url)
        assert response.status_code == 200

    def test_edit_profile_view_uses_correct_template(self, client, logged_in_user):
        url = reverse("user_management_app:edit_profile")
        response = client.get(url)
        assert "user_management_app/edit_profile.html" in [
            t.name for t in response.templates
        ]

    def test_edit_profile_view_contains_form_in_context(self, client, logged_in_user):
        url = reverse("user_management_app:edit_profile")
        response = client.get(url)
        assert "form" in response.context

    def test_edit_profile_view_redirects_for_anonymous_user(self, client):
        """
        Test that the profile view redirects an anonymous user:
        - Response has a status code of 302.
        - The user is redirected to the login page with the 'next' parameter set.
        """
        url = reverse("user_management_app:edit_profile")
        response = client.get(url)

        assert response.status_code == 302
        assert response.url == f"{reverse('user_management_app:login')}?next={url}"
