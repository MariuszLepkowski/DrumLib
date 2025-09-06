import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import resolve, reverse
from drummers.models import Drummer
from drummers.views import DrummerDetailView


@pytest.fixture
def test_drummer():
    return Drummer.objects.create(
        first_name="Vinnie",
        last_name="Colaiuta",
        bio="An amazing drummer known for his versatility.",
        slug="vinnie-colaiuta",
    )


@pytest.mark.django_db
class TestDrummerProfileView:
    def test_drummer_profile_view_resolves_to_correct_view(self, test_drummer):
        url = reverse(
            viewname="drummers:drummer_profile",
            kwargs={"slug": test_drummer.slug},
        )
        match = resolve(url)
        assert match.func.view_class == DrummerDetailView

    def test_drummer_profile_status_code(self, client, test_drummer):
        url = reverse("drummers:drummer_profile", kwargs={"slug": test_drummer.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_drummer_profile_view_uses_correct_template(self, client, test_drummer):
        url = reverse("drummers:drummer_profile", kwargs={"slug": test_drummer.slug})
        response = client.get(url)
        assert "drummers/drummer-profile.html" in (t.name for t in response.templates)

    def test_template_context(self, client, test_drummer):
        url = reverse("drummers:drummer_profile", kwargs={"slug": test_drummer.slug})
        response = client.get(url)

        assert "title" in response.context
        assert response.context["title"] == test_drummer.name
        assert "drummer" in response.context
        assert response.context["drummer"] == test_drummer
        assert "form" in response.context
        assert "comments" in response.context

    def test_post_comment_authenticated_user(
        self, client, test_drummer, django_user_model
    ):
        user = django_user_model.objects.create_user(
            username="testuser", password="password"
        )
        client.login(username="testuser", password="password")

        url = reverse("drummers:drummer_profile", kwargs={"slug": test_drummer.slug})
        data = {"text": "Great drummer!"}

        response = client.post(url, data)
        assert response.status_code == 302
        assert test_drummer.comment_set.filter(text="Great drummer!").exists()

    def test_post_comment_unauthenticated_user(self, client, test_drummer):
        url = reverse("drummers:drummer_profile", kwargs={"slug": test_drummer.slug})
        data = {"text": "Great drummer!"}

        response = client.post(url, data)

        assert response.status_code == 403
        assert not test_drummer.comment_set.filter(text="Great drummer!").exists()
