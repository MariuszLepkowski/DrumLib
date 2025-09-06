import pytest
from discography.models import Album
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from drummers.models import Drummer


@pytest.fixture
def drummer():
    return Drummer.objects.create(
        first_name="John", last_name="Bonham", slug="john-bonham"
    )


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
        url = reverse("discography:drummer_albums", kwargs={"slug": drummer.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_drummer_albums_404_for_nonexistent_drummer(self, client):
        url = reverse(
            "discography:drummer_albums", kwargs={"slug": "nonexistent-drummer"}
        )
        response = client.get(url)
        assert response.status_code == 404

    def test_drummer_albums_context(self, client, drummer, albums):
        url = reverse("discography:drummer_albums", kwargs={"slug": drummer.slug})
        response = client.get(url)
        sorted_albums = sorted(albums, key=lambda album: album.title)
        assert list(response.context["albums"]) == sorted_albums

    def test_drummer_albums_template_used(self, client, drummer):
        url = reverse("discography:drummer_albums", kwargs={"slug": drummer.slug})
        response = client.get(url)
        assert "discography/drummer-albums.html" in [t.name for t in response.templates]
