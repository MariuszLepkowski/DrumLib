import pytest
from drummers_app.models import Drummer

@pytest.mark.django_db
def test_drummer_str():
    drummer = Drummer.objects.create(name="Vinnie Colaiuta")
    assert str(drummer) == "Vinnie Colaiuta"