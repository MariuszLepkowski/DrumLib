import pytest
from comments_app.models import Comment
from django.urls import reverse


@pytest.mark.django_db
def test_edit_comment_authenticated(client, user, drummer, album):
    comment = Comment.objects.create(
        author=user, text="Old comment", drummer=drummer, album=album
    )
    client.force_login(user)
    url = reverse("comments_app:edit_comment", kwargs={"comment_id": comment.id})
    response = client.post(url, {"text": "Updated comment!"})

    comment.refresh_from_db()
    assert response.status_code == 302  # Redirect
    assert comment.text == "Updated comment!"


@pytest.mark.django_db
def test_edit_comment_unauthenticated(client, user, drummer, album):
    comment = Comment.objects.create(
        author=user, text="Old comment", drummer=drummer, album=album
    )
    url = reverse("comments_app:edit_comment", kwargs={"comment_id": comment.id})
    response = client.post(url, {"text": "Updated comment!"})

    comment.refresh_from_db()
    assert response.status_code == 302  # Redirect to login
    assert comment.text == "Old comment"


@pytest.mark.django_db
def test_edit_comment_not_author(client, user, another_user, drummer, album):
    comment = Comment.objects.create(
        author=another_user, text="Old comment", drummer=drummer, album=album
    )
    client.force_login(user)
    url = reverse("comments_app:edit_comment", kwargs={"comment_id": comment.id})
    response = client.post(url, {"text": "Updated comment!"})

    comment.refresh_from_db()
    assert response.status_code == 404
    assert comment.text == "Old comment"
