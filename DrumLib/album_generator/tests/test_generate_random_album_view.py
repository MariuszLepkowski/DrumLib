import pytest
from album_generator.views import generate_random_album
from discography.models import Album
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import resolve, reverse
from drummers.models import Drummer


@pytest.fixture
def drummer():
    return Drummer.objects.create(
        name="John Bonham", bio="Legendary drummer of Led Zeppelin."
    )


@pytest.fixture
def album(drummer):
    cover_image = SimpleUploadedFile(
        name="test_cover.jpg", content=b"test_image_content", content_type="image/jpeg"
    )
    album = Album.objects.create(
        title="Test Album", release_year=2020, album_cover=cover_image
    )
    album.drummers.add(drummer)
    return album


@pytest.mark.django_db
class TestGenerateRandomAlbumView:
    def test_generate_random_album_view_resolves_to_correct_view(self):
        url = reverse(viewname="album_generator:generate_random_album")
        assert resolve(url).func == generate_random_album

    def test_post_request_to_generate_random_album_view_returns_correct_status_code(
        self, client, drummer
    ):
        url = reverse(viewname="album_generator:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})
        assert response.status_code == 200

    def test_generate_random_album_view_uses_correct_template(self, client, drummer):
        url = reverse(viewname="album_generator:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})
        assert "album_generator/album-details.html" in [
            t.name for t in response.templates
        ]

    def test_generate_random_album_view_returns_valid_album_data_in_context(
        self, client, drummer, album
    ):
        url = reverse(viewname="album_generator:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})

        assert response.context["drummer"] == drummer
        assert response.context["album"] == album
        assert "tracks" in response.context
        assert "artists" in response.context

    def test_returns_album_when_albums_exist(self, client, drummer, album):
        album.drummers.add(drummer)

        url = reverse(viewname="album_generator:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})

        assert response.context["album"] == album

    def test_returns_none_when_no_albums_exist(self, client, drummer):
        url = reverse(viewname="album_generator:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})
        assert response.context["album"] is None

    def test_returns_404_with_invalid_drummer_id(self, client):
        url = reverse(viewname="album_generator:generate_random_album")
        response = client.post(url, {"drummer": 9999})
        assert response.status_code == 404

    def test_returns_404_when_no_drummer_id_provided(self, client):
        url = reverse(viewname="album_generator:generate_random_album")
        response = client.post(url, {})
        assert response.status_code == 400

    def test_returns_album_without_tracks_or_artists(self, client, drummer, album):
        album.tracks.clear()
        album.artists.clear()

        url = reverse(viewname="album_generator:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})

        assert response.context["album"] == album
        assert response.context["tracks"] is None
        assert response.context["artists"] is None
