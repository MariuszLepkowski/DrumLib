import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_view(client):
    url = reverse('home_app:home_page')
    response = client.get(url)
    assert response.status_code == 200
    assert "home_app/home-page.html" in [t.name for t in response.templates]
    assert b"Welcome to DrumLib!" in response.content
