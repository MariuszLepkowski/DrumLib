import pytest
from suggestions_app.forms import AlbumSuggestionForm, DrummerSuggestionForm


@pytest.mark.django_db
def test_drummer_suggestion_form_valid_data():
    form = DrummerSuggestionForm(data={"name": "John Bonham"})
    assert form.is_valid()


@pytest.mark.django_db
def test_drummer_suggestion_form_invalid_data():
    form = DrummerSuggestionForm(data={"name": ""})
    assert not form.is_valid()


@pytest.mark.django_db
def test_album_suggestion_form_valid_data():
    form = AlbumSuggestionForm(
        data={
            "album_author": "Led Zeppelin",
            "album_title": "Led Zeppelin IV",
            "drummers_on_album": "John Bonham",
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_album_suggestion_form_invalid_data():
    form = AlbumSuggestionForm(
        data={"album_author": "", "album_title": "", "drummers_on_album": ""}
    )
    assert not form.is_valid()
