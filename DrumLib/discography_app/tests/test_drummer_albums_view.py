import pytest
from django.urls import reverse
from drummers_app.models import Drummer
from discography_app.models import Album
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def drummer():
    return Drummer.objects.create(name="John Bonham")


@pytest.fixture
def albums(drummer):
    cover_image = SimpleUploadedFile(
        name="test_cover.jpg",
        content=b"test_image_content",
        content_type="image/jpeg",
    )
    album1 = Album.objects.create(
        title="Led Zeppelin IV",
        release_year=1971,
        album_cover=cover_image,
    )
    album2 = Album.objects.create(
        title="Led Zeppelin II",
        release_year=1969,
        album_cover=cover_image,
    )
    album1.drummers.add(drummer)
    album2.drummers.add(drummer)
    return [album1, album2]


@pytest.mark.django_db
class TestDrummerAlbumsView:
    def test_drummer_albums_status_code(self, client, drummer):
        url = reverse("discography_app:drummer_albums", kwargs={"drummer_name": drummer.name})
        response = client.get(url)
        assert response.status_code == 200

    def test_drummer_albums_404_for_nonexistent_drummer(self, client):
        url = reverse("discography_app:drummer_albums", kwargs={"drummer_name": "Nonexistent Drummer"})
        response = client.get(url)
        assert response.status_code == 404

    def test_drummer_albums_context(self, client, drummer, albums):
        url = reverse("discography_app:drummer_albums", kwargs={"drummer_name": drummer.name})
        response = client.get(url)
        assert "albums" in response.context

        # Sort the albums by title to match the view logic
        sorted_albums = sorted(albums, key=lambda album: album.title)
        assert list(response.context["albums"]) == sorted_albums

    def test_drummer_albums_template_used(self, client, drummer):
        url = reverse("discography_app:drummer_albums", kwargs={"drummer_name": drummer.name})
        response = client.get(url)
        assert "discography_app/drummer-albums.html" in [t.name for t in response.templates]
