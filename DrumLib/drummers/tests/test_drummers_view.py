import pytest
from django.urls import resolve, reverse
from drummers.models import Drummer
from drummers.views import DrummerListView


@pytest.mark.django_db
class TestDrummersView:
    def test_drummers_view_resolves_to_correct_view(self):
        url = reverse(viewname="drummers:drummer_list")
        assert resolve(url).func.view_class == DrummerListView

    def test_drummers_view_status_code(self, client):
        response = client.get(reverse("drummers:drummer_list"))
        assert response.status_code == 200

    def test_drummers_view_uses_correct_template(self, client):
        url = reverse(viewname="drummers:drummer_list")
        response = client.get(url)
        assert "drummers/drummers.html" in [t.name for t in response.templates]

    def test_drummers_view_sorted_content(self, client):
        """Test that the drummers view displays drummers sorted by last name."""
        Drummer.objects.create(first_name="Neil", last_name="Peart")
        Drummer.objects.create(first_name="Ginger", last_name="Baker")
        Drummer.objects.create(first_name="John", last_name="Bonham")

        response = client.get(reverse("drummers:drummer_list"))
        content = response.content.decode()

        # Check if names appear in the correct order
        assert content.index("Ginger Baker") < content.index("John Bonham")
        assert content.index("John Bonham") < content.index("Neil Peart")
