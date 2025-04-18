# from django.shortcuts import render
# from random import choice
# from drummers_app.models import Drummer
# from discography_app.models import Album
#
#
# def random_album(request):
#     drummers = Drummer.objects.all()
#     random_drummer = choice(drummers)
#     albums = Album.objects.filter(drummers=random_drummer).prefetch_related('artists')
#     random_album = choice(albums) if albums.exists() else None
#
#     if random_album:
#         artists = ', '.join(artist.name for artist in random_album.artists.all())
#     else:
#         artists = None
#
#     context = {
#         'title': 'Album Generator',
#         'drummer': random_drummer.name,
#         'album': random_album.title if random_album else 'No album found',
#         'artists': artists,
#     }
#
#     return render(request, 'album_generator_app/album-generator.html', context)
#
#


from django.shortcuts import render
from random import choice
from drummers_app.models import Drummer
from discography_app.models import Album, Track
from discography_app.utils import get_video_id
from django.http import Http404
from django.http import HttpResponseBadRequest


def album_generator_form(request):
    drummers = Drummer.objects.all()
    context = {
        'title': 'Album Generator',
        'drummers': drummers,
    }
    return render(request, 'album_generator_app/album-generator-form.html', context)


def generate_random_album(request):
    drummer_id = request.POST.get('drummer')

    if not drummer_id:
        return HttpResponseBadRequest("Drummer ID is required.")

    try:
        drummer = Drummer.objects.get(id=drummer_id)
    except Drummer.DoesNotExist:
        raise Http404("Drummer does not exist")

    albums = Album.objects.filter(drummers=drummer)
    random_album = choice(albums) if albums.exists() else None

    if random_album and random_album.tracks.exists():
        tracks = Track.objects.filter(albums=random_album, drummers=drummer)

        for track in tracks:
            track.video_id = get_video_id(track.track_url)

    else:
        tracks = None

    if random_album and random_album.artists.exists():
        artists = ', '.join(artist.name for artist in random_album.artists.all())
    else:
        artists = None

    context = {
        'title': 'Album Generator',
        'drummer': drummer,
        'album': random_album,
        'artists': artists,
        'tracks': tracks,
    }

    return render(request, 'album_generator_app/album-details.html', context)

