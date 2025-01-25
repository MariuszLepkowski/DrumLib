import pytest
from suggestions_app.models import DrummerSuggestion, AlbumSuggestion


@pytest.mark.django_db
def test_drummer_suggestion_creation(user):
    suggestion = DrummerSuggestion.objects.create(
        name="John Bonham",
        suggested_by=user
    )

    assert suggestion.name == "John Bonham"
    assert suggestion.suggested_by == user
    assert not suggestion.is_reviewed


@pytest.mark.django_db
def test_album_suggestion_creation(user):
    suggestion = AlbumSuggestion.objects.create(
        album_author="Led Zeppelin",
        album_title="Led Zeppelin IV",
        drummers_on_album="John Bonham",
        suggested_by=user
    )

    assert suggestion.album_author == "Led Zeppelin"
    assert suggestion.album_title == "Led Zeppelin IV"
    assert suggestion.drummers_on_album == "John Bonham"
    assert suggestion.suggested_by == user
    assert not suggestion.is_reviewed


@pytest.mark.django_db
def test_drummer_suggestion_str_method(user):
    suggestion = DrummerSuggestion.objects.create(name="John Bonham", suggested_by=user)
    assert str(suggestion) == "John Bonham"


@pytest.mark.django_db
def test_album_suggestion_str_method(user):
    suggestion = AlbumSuggestion.objects.create(
        album_author="Led Zeppelin",
        album_title="Led Zeppelin IV",
        drummers_on_album="John Bonham",
        suggested_by=user
    )
    assert str(suggestion) == "Led Zeppelin IV"
