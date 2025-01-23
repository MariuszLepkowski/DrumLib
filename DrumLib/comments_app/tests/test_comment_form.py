from comments_app.forms import CommentForm


def test_comment_form_valid_data():
    form = CommentForm(data={"text": "This is a test comment"})
    assert form.is_valid()


def test_comment_form_invalid_data():
    form = CommentForm(data={"text": ""})  # Text is required
    assert not form.is_valid()


def test_comment_form_widget():
    form = CommentForm()
    assert form.fields["text"].widget.attrs["placeholder"] == "Write your comment here..."
