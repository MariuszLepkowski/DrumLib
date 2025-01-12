import pytest
from django.urls import reverse, resolve
from album_generator_app.views import album_generator_form


class TestAlbumGeneratorFormView:
    def test_album_generator_form_view_resolves_to_correct_view(self):
        url = reverse(viewname="album_generator_app:album_generator_form")
        assert resolve(url).func == album_generator_form