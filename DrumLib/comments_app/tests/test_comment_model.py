import pytest
from comments_app.models import Comment


@pytest.mark.django_db
def test_comment_creation(user, drummer, album):
    comment = Comment.objects.create(
        author=user,
        text="Great drummer!",
        drummer=drummer,
        album=album
    )
    assert comment.text == "Great drummer!"
    assert comment.author == user
    assert comment.drummer == drummer
    assert comment.album == album
    assert comment.__str__() == f'Comment by {user} on {comment.created_at}: Great drummer!'
