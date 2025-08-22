import pytest
from discography_app.models import Track, Artist
from drummers_app.models import Drummer


@pytest.fixture
def drummer():
    return Drummer.objects.create(name="John Bonham", bio="Legendary drummer of Led Zeppelin.")


@pytest.fixture
def artist():
    return Artist.objects.create(name="Led Zeppelin")


@pytest.fixture
def track(drummer, artist):
    track = Track.objects.create(title="Stairway to Heaven", track_url="https://example.com/track")
    track.artists.add(artist)
    track.drummers.add(drummer)
    return track


@pytest.mark.django_db
class TestTrackModel:
    def test_track_creation(self, track):
        assert track.title == "Stairway to Heaven"
        assert track.track_url == "https://example.com/track"
        assert track.artists.count() == 1
        assert track.drummers.count() == 1

    def test_track_str_method(self, track):
        assert str(track) == "Stairway to Heaven"

    def test_track_with_no_url(self, artist, drummer):
        track = Track.objects.create(title="Black Dog")
        track.artists.add(artist)
        track.drummers.add(drummer)

        assert track.title == "Black Dog"
        assert track.track_url is None

    def test_track_multiple_artists_and_drummers(self):
        artist1 = Artist.objects.create(name="The Beatles")
        artist2 = Artist.objects.create(name="The Rolling Stones")
        drummer1 = Drummer.objects.create(name="Ringo Starr")
        drummer2 = Drummer.objects.create(name="Charlie Watts")

        track = Track.objects.create(title="Come Together")
        track.artists.add(artist1, artist2)
        track.drummers.add(drummer1, drummer2)

        assert track.artists.count() == 2
        assert track.drummers.count() == 2
