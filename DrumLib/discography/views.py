from comments.forms import CommentForm
from comments.models import Comment
from django.shortcuts import get_object_or_404, redirect, render
from drummers.models import Drummer
from drummers.views import sort_by_last_name

from .models import Album, Track
from .utils import get_video_id


def drummers_list(request):
    drummers = Drummer.objects.all().order_by("name")
    drummers_sorted = sorted(drummers, key=sort_by_last_name)

    context = {
        "title": "Discographies",
        "drummers": drummers_sorted,
    }
    return render(request, "discography_app/drummers-list.html", context)


def drummer_albums(request, drummer_name):
    drummer = get_object_or_404(Drummer, name=drummer_name)
    albums = (
        Album.objects.filter(drummers=drummer)
        .order_by("title")
        .prefetch_related("artists")
    )

    context = {
        "title": f"{drummer}'s albums",
        "drummer": drummer,
        "albums": albums,
    }
    return render(request, "discography_app/drummer-albums.html", context)


def drummer_tracks(request, drummer_name):
    drummer = get_object_or_404(Drummer, name=drummer_name)
    tracks = (
        Track.objects.filter(drummers=drummer)
        .prefetch_related("artists")
        .order_by("artists__name")
    )

    for track in tracks:
        track.video_id = get_video_id(track.track_url)

    context = {
        "title": f"{drummer}'s tracks",
        "drummer": drummer,
        "tracks": tracks,
    }
    return render(request, "discography_app/drummer-tracks.html", context)


def album_tracks(request, album_title, drummer_name):
    drummer = get_object_or_404(Drummer, name=drummer_name)
    album = get_object_or_404(Album, title=album_title)
    tracks = Track.objects.filter(albums=album, drummers=drummer)
    artists = album.artists.all()

    for track in tracks:
        track.video_id = get_video_id(track.track_url)

    comments = Comment.objects.filter(album=album, drummer=drummer)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.album = album
            comment.drummer = drummer
            comment.save()

            return redirect(
                "discography_app:album_tracks",
                album_title=album.title,
                drummer_name=drummer.name,
            )

    context = {
        "title": album_title,
        "tracks": tracks,
        "artists": artists,
        "album": album,
        "drummer": drummer,
        "form": form,
        "comments": comments,
    }

    return render(request, "discography_app/album-tracks.html", context)
