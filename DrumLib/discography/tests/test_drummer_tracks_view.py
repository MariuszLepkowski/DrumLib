import pytest
from discography.models import Artist, Track
from django.urls import reverse
from drummers.models import Drummer


@pytest.fixture
def drummer(db):
    return Drummer.objects.create(name="John Bonham")


@pytest.fixture
def artists(db):
    artist1 = Artist.objects.create(name="Led Zeppelin")
    artist2 = Artist.objects.create(name="Solo Project")
    return [artist1, artist2]


@pytest.fixture
def tracks(db, drummer, artists):
    track1 = Track.objects.create(
        title="Whole Lotta Love", track_url="http://example.com/track1"
    )
    track2 = Track.objects.create(
        title="Moby Dick", track_url="http://example.com/track2"
    )

    track1.artists.add(artists[0])
    track1.drummers.add(drummer)

    track2.artists.add(artists[1])
    track2.drummers.add(drummer)

    return [track1, track2]


@pytest.mark.django_db
class TestDrummerTracksView:
    def test_drummer_tracks_status_code(self, client, drummer):
        url = reverse(
            "discography:drummer_tracks", kwargs={"drummer_name": drummer.name}
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_drummer_tracks_context(self, client, drummer, tracks):
        url = reverse(
            "discography:drummer_tracks", kwargs={"drummer_name": drummer.name}
        )
        response = client.get(url)
        assert "tracks" in response.context
        assert response.context["drummer"] == drummer

        sorted_tracks = sorted(
            tracks,
            key=lambda track: (
                track.artists.first().name if track.artists.exists() else ""
            ),
        )
        assert list(response.context["tracks"]) == sorted_tracks

    def test_drummer_tracks_template_used(self, client, drummer):
        url = reverse(
            "discography:drummer_tracks", kwargs={"drummer_name": drummer.name}
        )
        response = client.get(url)
        assert response.status_code == 200
        assert "discography/drummer-tracks.html" in [t.name for t in response.templates]
