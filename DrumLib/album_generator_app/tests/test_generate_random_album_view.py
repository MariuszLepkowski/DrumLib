import pytest
from django.urls import reverse, resolve
from album_generator_app.views import generate_random_album
from drummers_app.models import Drummer
from discography_app.models import Album
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def drummer():
    return Drummer.objects.create(name="John Bonham", bio="Legendary drummer of Led Zeppelin.")


@pytest.fixture
def album(drummer):
    cover_image = SimpleUploadedFile(
        name='test_cover.jpg',
        content=b'test_image_content',
        content_type='image/jpeg'
    )
    album = Album.objects.create(
        title="Test Album",
        release_year=2020,
        album_cover=cover_image
    )
    album.drummers.add(drummer)
    return album


@pytest.mark.django_db
class TestGenerateRandomAlbumView:
    def test_generate_random_album_view_resolves_to_correct_view(self):
        url = reverse(viewname="album_generator_app:generate_random_album")
        assert resolve(url).func == generate_random_album

    def test_post_request_to_generate_random_album_view_returns_correct_status_code(self, client, drummer):
        url = reverse(viewname="album_generator_app:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})
        assert response.status_code == 200

    def test_generate_random_album_view_uses_correct_template(self, client, drummer):
        url = reverse(viewname="album_generator_app:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})
        assert 'album_generator_app/album-details.html' in [t.name for t in response.templates]

    def test_generate_random_album_view_returns_valid_album_data_in_context(self, client, drummer, album):
        url = reverse(viewname="album_generator_app:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})

        assert response.context["drummer"] == drummer
        assert response.context["album"] == album
        assert "tracks" in response.context
        assert "artists" in response.context

    def test_returns_album_when_albums_exist(self, client, drummer, album):
        album.drummers.add(drummer)

        url = reverse(viewname="album_generator_app:generate_random_album")
        response = client.post(url, {"drummer": drummer.id})

        assert response.context["album"] == album
