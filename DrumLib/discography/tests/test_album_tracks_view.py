import pytest
from comments.forms import CommentForm
from comments.models import Comment
from discography.models import Album, Artist, Track
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from drummers.models import Drummer


@pytest.fixture
def drummer(db):
    return Drummer.objects.create(
        first_name="John", last_name="Bonham", slug="john-bonham"
    )


@pytest.fixture
def artists(db):
    artist = Artist.objects.create(name="Led Zeppelin")
    return [artist]


@pytest.fixture
def album(db, drummer, artists):
    album_cover = SimpleUploadedFile(
        "test_cover.jpg", b"file_content", content_type="image/jpeg"
    )
    album = Album.objects.create(
        title="Led Zeppelin IV",
        release_year=1971,
        genre="Rock",
        album_url="http://example.com/album",
        album_cover=album_cover,
    )
    album.drummers.add(drummer)
    album.artists.add(*artists)
    return album


@pytest.fixture
def tracks(db, album, drummer):
    track = Track.objects.create(
        title="Stairway to Heaven", track_url="http://example.com/track"
    )
    track.albums.add(album)
    track.drummers.add(drummer)
    return [track]


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def comments(db, album, drummer, user):
    return [
        Comment.objects.create(
            album=album, drummer=drummer, author=user, text="Amazing album!"
        ),
        Comment.objects.create(
            album=album,
            drummer=drummer,
            author=user,
            text="My favorite tracks are here.",
        ),
    ]


@pytest.mark.django_db
class TestAlbumTracksView:
    def test_album_tracks_status_code(self, client, drummer, album):
        url = reverse(
            "discography:album_tracks",
            kwargs={"album_title": album.title, "slug": drummer.slug},
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_album_tracks_context(self, client, drummer, album, tracks, comments):
        url = reverse(
            "discography:album_tracks",
            kwargs={"album_title": album.title, "slug": drummer.slug},
        )
        response = client.get(url)

        assert response.context["album"] == album
        assert response.context["drummer"] == drummer
        assert list(response.context["tracks"]) == tracks
        assert list(response.context["artists"]) == list(album.artists.all())
        assert list(response.context["comments"]) == comments
        assert isinstance(response.context["form"], CommentForm)

    def test_album_tracks_template_used(self, client, drummer, album):
        url = reverse(
            "discography:album_tracks",
            kwargs={"album_title": album.title, "slug": drummer.slug},
        )
        response = client.get(url)
        assert "discography/album-tracks.html" in [t.name for t in response.templates]

    def test_album_tracks_post_comment(self, client, drummer, album, user):
        client.login(username="testuser", password="password123")
        url = reverse(
            "discography:album_tracks",
            kwargs={"album_title": album.title, "slug": drummer.slug},
        )
        data = {"text": "New comment"}
        response = client.post(url, data)

        assert response.status_code == 302
        assert Comment.objects.filter(
            text="New comment", album=album, drummer=drummer
        ).exists()
