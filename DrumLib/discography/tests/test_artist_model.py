import pytest
from discography_app.models import Artist
from drummers_app.models import Drummer


@pytest.fixture
def drummer():
    return Drummer.objects.create(name="John Bonham", bio="Legendary drummer of Led Zeppelin.")


@pytest.fixture
def artist(drummer):
    artist = Artist.objects.create(name="Led Zeppelin")
    artist.collaborating_drummers.add(drummer)
    return artist


@pytest.mark.django_db
class TestArtistModel:
    def test_artist_creation(self, artist):
        assert artist.name == "Led Zeppelin"
        assert artist.collaborating_drummers.count() == 1

    def test_artist_str_method(self, artist):
        assert str(artist) == "Led Zeppelin"

    def test_artist_name_uniqueness(self):
        Artist.objects.create(name="Pink Floyd")
        with pytest.raises(Exception):
            Artist.objects.create(name="Pink Floyd")  # Should raise IntegrityError
