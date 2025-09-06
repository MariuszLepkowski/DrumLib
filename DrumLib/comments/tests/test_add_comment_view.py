import pytest
from comments.models import Comment
from django.urls import reverse


@pytest.mark.django_db
def test_add_comment_drummer_authenticated(client, user, drummer):
    client.force_login(user)
    url = reverse(
        "comments:add_comment",
        kwargs={"content_type": "drummer", "object_id": drummer.pk},
    )
    response = client.post(url, {"text": "Amazing drummer!"})

    assert response.status_code == 302  # Redirect
    assert Comment.objects.filter(
        text="Amazing drummer!", author=user, drummer=drummer
    ).exists()


@pytest.mark.django_db
def test_add_comment_album_authenticated(client, user, album, drummer):
    client.force_login(user)
    url = reverse(
        "comments:add_comment",
        kwargs={"content_type": "album", "object_id": album.pk},
    )
    response = client.post(
        url, {"text": "Fantastic album!", "drummer_slug": drummer.slug}
    )

    assert response.status_code == 302  # Redirect
    assert Comment.objects.filter(
        text="Fantastic album!", author=user, album=album
    ).exists()


@pytest.mark.django_db
def test_add_comment_unauthenticated(client, drummer):
    url = reverse(
        "comments:add_comment",
        kwargs={"content_type": "drummer", "object_id": drummer.pk},
    )
    response = client.post(url, {"text": "Amazing drummer!"})

    assert response.status_code == 302  # Redirect to login
    assert Comment.objects.count() == 0
