import pytest
from django.urls import reverse
from suggestions_app.models import DrummerSuggestion, AlbumSuggestion


@pytest.mark.django_db
def test_suggest_drummer_authenticated(client, user):
    client.force_login(user)
    url = reverse('suggestions_app:suggest_drummer')
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_suggest_drummer_post_valid(client, user):
    client.force_login(user)
    url = reverse('suggestions_app:suggest_drummer')
    response = client.post(url, {'name': 'John Bonham'})

    assert response.status_code == 302  # Redirect to thank you page
    assert DrummerSuggestion.objects.filter(name='John Bonham', suggested_by=user).exists()


@pytest.mark.django_db
def test_suggest_drummer_post_invalid(client, user):
    client.force_login(user)
    url = reverse('suggestions_app:suggest_drummer')
    response = client.post(url, {'name': ''})  # Puste pole

    assert response.status_code == 200  # Formularz zostanie ponownie wyświetlony
    assert not DrummerSuggestion.objects.exists()


@pytest.mark.django_db
def test_suggest_album_authenticated(client, user):
    client.force_login(user)
    url = reverse('suggestions_app:suggest_album')
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_suggest_album_post_valid(client, user):
    client.force_login(user)
    url = reverse('suggestions_app:suggest_album')
    data = {
        'album_author': 'Led Zeppelin',
        'album_title': 'Led Zeppelin IV',
        'drummers_on_album': 'John Bonham'
    }
    response = client.post(url, data)

    assert response.status_code == 302  # Redirect to thank you page
    assert AlbumSuggestion.objects.filter(album_title='Led Zeppelin IV', suggested_by=user).exists()


@pytest.mark.django_db
def test_suggest_album_post_invalid(client, user):
    client.force_login(user)
    url = reverse('suggestions_app:suggest_album')
    data = {
        'album_author': '',
        'album_title': '',
        'drummers_on_album': ''
    }
    response = client.post(url, data)

    assert response.status_code == 200  # Formularz zostanie ponownie wyświetlony
    assert not AlbumSuggestion.objects.exists()


@pytest.mark.django_db
def test_suggestions_thank_you_authenticated(client, user):
    client.force_login(user)
    url = reverse('suggestions_app:suggestions_thank_you')
    response = client.get(url)

    assert response.status_code == 200
    assert b'Thanks For Your Suggestion!' in response.content


@pytest.mark.django_db
def test_suggest_drummer_unauthenticated(client):
    url = reverse('suggestions_app:suggest_drummer')
    response = client.get(url)

    assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
def test_suggest_album_unauthenticated(client):
    url = reverse('suggestions_app:suggest_album')
    response = client.get(url)

    assert response.status_code == 302  # Redirect to login
