import pytest
from django.urls import reverse, resolve
from drummers_app.views import drummer_profile
from drummers_app.models import Drummer
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

@pytest.fixture
def test_drummer():
    return Drummer.objects.create(
        name="Vinnie Colaiuta",
        bio="An amazing drummer known for his versatility."
    )


@pytest.mark.django_db
class TestDrummerProfileView:
    def test_drummer_profile_view_resolves_to_correct_view(self, test_drummer):
        url = reverse(viewname="drummers_app:drummer_profile", kwargs={"drummer_name": test_drummer.name})
        assert resolve(url).func == drummer_profile

    def test_drummer_profile_status_code(self, test_drummer):
        factory = RequestFactory()
        request = factory.get(reverse("drummers_app:drummer_profile", kwargs={"drummer_name": test_drummer.name}))
        request.user = AnonymousUser()

        response = drummer_profile(request, drummer_name=test_drummer.name)
        assert response.status_code == 200

    def test_drummer_profile_view_uses_correct_template(self, client, test_drummer):
        response = client.get(reverse('drummers_app:drummer_profile', args=[test_drummer.name]))
        assert 'drummers_app/drummer-profile.html' in (t.name for t in response.templates)

    def test_template_context(self, client, test_drummer):
        url = reverse("drummers_app:drummer_profile", kwargs={"drummer_name": test_drummer.name})
        response = client.get(url)

        assert "title" in response.context
        assert response.context["title"] == test_drummer.name
        assert "drummer" in response.context
        assert response.context["drummer"] == test_drummer
        assert "form" in response.context
        assert "comments" in response.context

    def test_post_comment_authenticated_user(self, client, test_drummer, django_user_model):
        user = django_user_model.objects.create_user(username="testuser", password="password")
        client.login(username="testuser", password="password")

        url = reverse("drummers_app:drummer_profile", kwargs={"drummer_name": test_drummer.name})
        data = {"text": "Great drummer!"}

        response = client.post(url, data)
        assert response.status_code == 302
        assert test_drummer.comment_set.filter(text="Great drummer!").exists()

    def test_post_comment_unauthenticated_user(self, client, test_drummer):
        url = reverse("drummers_app:drummer_profile", kwargs={"drummer_name": test_drummer.name})
        data = {"text": "Great drummer!"}

        response = client.post(url, data)

        assert response.status_code == 403
        assert not test_drummer.comment_set.filter(text="Great drummer!").exists()