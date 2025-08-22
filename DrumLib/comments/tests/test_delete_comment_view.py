import pytest
from comments.models import Comment
from django.urls import reverse


@pytest.mark.django_db
def test_delete_comment_authenticated_author(client, user, drummer, album):
    comment = Comment.objects.create(
        author=user, text="Comment to delete", drummer=drummer, album=album
    )
    client.force_login(user)
    url = reverse("comments:delete_comment", kwargs={"comment_id": comment.id})
    response = client.post(url)

    assert response.status_code == 302  # Redirect
    assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_delete_comment_authenticated_staff(client, staff_user, user, drummer, album):
    comment = Comment.objects.create(
        author=user, text="Comment to delete", drummer=drummer, album=album
    )
    client.force_login(staff_user)
    url = reverse("comments:delete_comment", kwargs={"comment_id": comment.id})
    response = client.post(url)

    assert response.status_code == 302  # Redirect
    assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_delete_comment_unauthenticated(client, user, drummer, album):
    comment = Comment.objects.create(
        author=user, text="Comment to delete", drummer=drummer, album=album
    )
    url = reverse("comments:delete_comment", kwargs={"comment_id": comment.id})
    response = client.post(url)

    assert response.status_code == 302  # Redirect to login
    assert Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_delete_comment_not_author(client, user, another_user, drummer, album):
    comment = Comment.objects.create(
        author=another_user, text="Comment to delete", drummer=drummer, album=album
    )
    client.force_login(user)
    url = reverse("comments:delete_comment", kwargs={"comment_id": comment.id})
    response = client.post(url)

    assert response.status_code == 302  # Redirect
    assert Comment.objects.filter(id=comment.id).exists()
