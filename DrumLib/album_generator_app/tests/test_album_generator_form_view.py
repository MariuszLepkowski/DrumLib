import pytest
from django.urls import reverse, resolve
from album_generator_app.views import album_generator_form


@pytest.mark.django_db
class TestAlbumGeneratorFormView:
    def test_album_generator_form_view_resolves_to_correct_view(self):
        url = reverse(viewname="album_generator_app:album_generator_form")
        assert resolve(url).func == album_generator_form

    def test_album_generator_form_view_uses_correct_template(self, client):
        url = reverse(viewname="album_generator_app:album_generator_form")
        response = client.get(url)
        assert 'album_generator_app/album-generator-form.html' in [t.name for t in response.templates]
