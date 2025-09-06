import pytest
from album_generator.views import album_generator_form
from django.urls import resolve, reverse
from drummers.models import Drummer


@pytest.mark.django_db
class TestAlbumGeneratorFormView:
    def test_album_generator_form_view_resolves_to_correct_view(self):
        url = reverse(viewname="album_generator:album_generator_form")
        assert resolve(url).func == album_generator_form

    def test_album_generator_form_view_status_code(self, client):
        url = reverse(viewname="album_generator:album_generator_form")
        response = client.get(url)
        assert response.status_code == 200

    def test_album_generator_form_view_uses_correct_template(self, client):
        url = reverse(viewname="album_generator:album_generator_form")
        response = client.get(url)
        assert "album_generator/album-generator-form.html" in [
            t.name for t in response.templates
        ]

    def test_album_generator_form_view_context_has_drummer_list(self, client):
        url = reverse(viewname="album_generator:album_generator_form")

        Drummer.objects.create(
            first_name="John",
            last_name="Bonham",
            bio="Legendary drummer of Led Zeppelin.",
        )
        Drummer.objects.create(
            first_name="Neil", last_name="Peart", bio="Iconic drummer of Rush."
        )

        response = client.get(url)
        assert "drummers" in response.context

        drummers = response.context["drummers"]
        assert drummers.count() == 2
        assert any(d.slug == "john-bonham" for d in drummers)
        assert any(d.slug == "neil-peart" for d in drummers)
