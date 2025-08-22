import pytest
from django.urls import reverse
from drummers.models import Drummer


@pytest.fixture
def drummers():
    return [
        Drummer.objects.create(name="John Bonham"),
        Drummer.objects.create(name="Neil Peart"),
        Drummer.objects.create(name="Phil Collins"),
    ]


@pytest.mark.django_db
class TestDrummersListView:
    def test_drummers_list_status_code(self, client, drummers):
        url = reverse("discography:drummers_list")
        response = client.get(url)
        assert response.status_code == 200

    def test_drummers_list_context(self, client, drummers):
        url = reverse("discography:drummers_list")
        response = client.get(url)
        assert "drummers" in response.context
        drummers_sorted = sorted(drummers, key=lambda d: d.name.split()[-1])
        assert list(response.context["drummers"]) == drummers_sorted

    def test_drummers_list_template_used(self, client):
        url = reverse("discography:drummers_list")
        response = client.get(url)
        assert "discography/drummers-list.html" in [t.name for t in response.templates]
