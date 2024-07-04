from django.shortcuts import render
from random import choice
from drummers_app.models import Drummer
from discography_app.models import Album


def random_album(request):
    drummers = Drummer.objects.all()
    random_drummer = choice(drummers)
    albums = Album.objects.filter(drummers=random_drummer)
    album = choice(albums) if albums.exists() else None

    context = {
        'title': 'Album Generator',
        'drummer': random_drummer.name,
        'album': album.title if album else 'No album found',
    }

    return render(request, 'album_generator_app/album-generator.html', context)


