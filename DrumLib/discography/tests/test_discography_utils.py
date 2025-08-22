import pytest
from discography.utils import get_video_id


@pytest.mark.parametrize(
    "url, expected_video_id",
    [
        ("https://www.youtube.com/watch?v=abc123", "abc123"),
        ("https://youtu.be/abc123?v=xyz456", "xyz456"),
        ("https://www.youtube.com/watch?v=def456&feature=youtu.be", "def456"),
        ("https://www.youtube.com/watch", None),
        ("invalid-url", None),
    ],
)
def test_get_video_id(url, expected_video_id):
    assert get_video_id(url) == expected_video_id
