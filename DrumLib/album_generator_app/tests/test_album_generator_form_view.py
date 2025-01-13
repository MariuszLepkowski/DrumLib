import pytest
from django.urls import reverse, resolve
from album_generator_app.views import album_generator_form
from drummers_app.models import Drummer


@pytest.mark.django_db
class TestAlbumGeneratorFormView:
    def test_album_generator_form_view_resolves_to_correct_view(self):
        url = reverse(viewname="album_generator_app:album_generator_form")
        assert resolve(url).func == album_generator_form

    def test_album_generator_form_view_status_code(self, client):
        url = reverse(viewname="album_generator_app:album_generator_form")
        response = client.get(url)
        assert response.status_code == 200

    def test_album_generator_form_view_uses_correct_template(self, client):
        url = reverse(viewname="album_generator_app:album_generator_form")
        response = client.get(url)
        assert 'album_generator_app/album-generator-form.html' in [t.name for t in response.templates]

    def test_album_generator_form_view_context_has_drummer_list(self, client):
        url = reverse(viewname="album_generator_app:album_generator_form")

        Drummer.objects.create(name="John Bonham", bio="Legendary drummer of Led Zeppelin.")
        Drummer.objects.create(name="Neil Peart", bio="Iconic drummer of Rush.")

        response = client.get(url)
        assert 'drummers' in response.context

        drummers = response.context['drummers']
        assert drummers.count() == 2
        assert any(d.name == "John Bonham" for d in drummers)
        assert any(d.name == "Neil Peart" for d in drummers)