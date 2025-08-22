import pytest
from discography_app.models import Album, Artist, Track
from django.core.files.uploadedfile import SimpleUploadedFile
from drummers_app.models import Drummer


@pytest.fixture
def album_cover():
    return SimpleUploadedFile(
        name="test_cover.jpg", content=b"test_image_content", content_type="image/jpeg"
    )


@pytest.fixture
def artist():
    return Artist.objects.create(name="Test Artist")


@pytest.fixture
def drummer():
    return Drummer.objects.create(name="Test Drummer", bio="Bio for test drummer.")


@pytest.fixture
def track():
    return Track.objects.create(title="Test Track")


@pytest.fixture
def album(album_cover, artist, drummer, track):
    album = Album.objects.create(
        title="Test Album", release_year=2020, genre="Rock", album_cover=album_cover
    )
    album.artists.add(artist)
    album.drummers.add(drummer)
    album.tracks.add(track)
    return album


@pytest.mark.django_db
class TestAlbumModel:
    def test_album_creation(self, album):
        assert album.title == "Test Album"
        assert album.release_year == 2020
        assert album.genre == "Rock"
        assert "test_cover" in album.album_cover.name

    def test_album_relations(self, album, artist, drummer, track):
        assert artist in album.artists.all()
        assert drummer in album.drummers.all()
        assert track in album.tracks.all()

    def test_album_str_method(self, album):
        assert str(album) == "Test Album"
