import pytest
from drummers_app.views import drummers
from django.urls import reverse, resolve



@pytest.mark.django_db
class TestDrummersView:
    def test_drummers_view_resolves_to_correct_view(self):
        url = reverse(viewname="drummers_app:drummers_list")
        assert resolve(url).func == drummers

    def test_drummers_view_uses_correct_template(self, client):
        url = reverse(viewname="drummers_app:drummers_list")
        response = client.get(url)
        assert 'drummers_app/drummers.html' in [t.name for t in response.templates]

