import pytest
from django.urls import resolve, reverse
from drummers.models import Drummer
from drummers.views import drummers


@pytest.mark.django_db
class TestDrummersView:
    def test_drummers_view_resolves_to_correct_view(self):
        url = reverse(viewname="drummers:drummers_list")
        assert resolve(url).func == drummers

    def test_drummers_view_status_code(self, client):
        response = client.get(reverse("drummers:drummers_list"))
        assert response.status_code == 200

    def test_drummers_view_uses_correct_template(self, client):
        url = reverse(viewname="drummers:drummers_list")
        response = client.get(url)
        assert "drummers/drummers.html" in [t.name for t in response.templates]

    def test_drummers_view_sorted_content(self, client):
        """
        Test that the drummers view displays drummers sorted by last name.
        """
        Drummer.objects.create(name="Neil Peart")
        Drummer.objects.create(name="Ginger Baker")
        Drummer.objects.create(name="John Bonham")

        response = client.get(reverse("drummers:drummers_list"))
        content = response.content.decode()

        # Check if names appear in the correct order
        assert content.index("Ginger Baker") < content.index("John Bonham")
        assert content.index("John Bonham") < content.index("Neil Peart")
