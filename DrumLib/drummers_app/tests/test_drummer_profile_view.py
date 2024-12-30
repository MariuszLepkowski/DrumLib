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

