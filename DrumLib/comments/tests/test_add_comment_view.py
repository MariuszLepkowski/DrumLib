import pytest
from comments_app.models import Comment
from django.urls import reverse


@pytest.mark.django_db
def test_add_comment_drummer_authenticated(client, user, drummer):
    client.force_login(user)
    url = reverse(
        "comments_app:add_comment",
        kwargs={"content_type": "drummer", "object_id": drummer.id},
    )
    response = client.post(url, {"text": "Amazing drummer!"})

    assert response.status_code == 302  # Redirect
    assert Comment.objects.filter(
        text="Amazing drummer!", author=user, drummer=drummer
    ).exists()


@pytest.mark.django_db
def test_add_comment_album_authenticated(client, user, album):
    client.force_login(user)
    url = reverse(
        "comments_app:add_comment",
        kwargs={"content_type": "album", "object_id": album.id},
    )
    response = client.post(
        url, {"text": "Fantastic album!", "drummer_name": "John Bonham"}
    )

    assert response.status_code == 302  # Redirect
    assert Comment.objects.filter(
        text="Fantastic album!", author=user, album=album
    ).exists()


@pytest.mark.django_db
def test_add_comment_unauthenticated(client, drummer):
    url = reverse(
        "comments_app:add_comment",
        kwargs={"content_type": "drummer", "object_id": drummer.id},
    )
    response = client.post(url, {"text": "Amazing drummer!"})

    assert response.status_code == 302  # Redirect to login
    assert Comment.objects.count() == 0
