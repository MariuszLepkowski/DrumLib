from django.shortcuts import render, get_object_or_404
from .models import Album, Track
from drummers_app.models import Drummer
from drummers_app.views import sort_by_last_name


def drummers_list(request):
    drummers = Drummer.objects.all().order_by('name')
    drummers_sorted = sorted(drummers, key=sort_by_last_name)

    context = {
        'title': 'Discographies',
        'drummers': drummers_sorted,
    }
    return render(request, 'discography_app/drummers-list.html', context)


def drummer_albums(request, drummer_name):
    drummer = get_object_or_404(Drummer, name=drummer_name)
    albums = Album.objects.filter(drummers=drummer).order_by('title').prefetch_related('artists')

    context = {
        'title': f"{drummer}'s albums",
        'drummer': drummer,
        'albums': albums,
    }
    return render(request, 'discography_app/drummer-albums.html', context)


def drummer_tracks(request, drummer_name):
    drummer = get_object_or_404(Drummer, name=drummer_name)
    tracks = Track.objects.filter(drummers=drummer).order_by('title')

    context = {
        'title': f"{drummer}'s tracks",
        'drummer': drummer,
        'tracks': tracks,
    }
    return render(request, 'discography_app/drummer-tracks.html', context)


def album_tracks(request, album_title):
    album = get_object_or_404(Album, title=album_title)
    tracks = album.tracks.all()

    context = {
        'title': album_title,
        'tracks': tracks,
    }

    return render(request, 'discography_app/album-tracks.html', context)