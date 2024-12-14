import pytest
from django.urls import reverse, resolve
from drummers_app.views import drummer_profile
from drummers_app.models import Drummer

@pytest.fixture
def test_drummer():
    return Drummer.objects.create(name="Vinnie Colaiuta")

@pytest.mark.django_db
class TestDrummerProfileView:
    def test_drummer_profile_view_resolves_to_correct_view(self, test_drummer):
        url = reverse(viewname="drummers_app:drummer_profile", kwargs={"drummer_name": test_drummer.name})
        assert resolve(url).func == drummer_profile
