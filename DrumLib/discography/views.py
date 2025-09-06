from comments.forms import CommentForm
from comments.models import Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from drummers.models import Drummer

from .models import Album, Track
from .utils import get_video_id


class DrummerListView(ListView):
    model = Drummer
    template_name = "discography/drummers-list.html"
    context_object_name = "drummers"

    def get_queryset(self):
        return Drummer.objects.all().order_by("last_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Discographies"
        return context


class DrummerAlbumsView(ListView):
    model = Album
    template_name = "discography/drummer-albums.html"
    context_object_name = "albums"

    def get_queryset(self):
        self.drummer = get_object_or_404(Drummer, slug=self.kwargs["slug"])
        return (
            Album.objects.filter(drummers=self.drummer)
            .order_by("title")
            .prefetch_related("artists")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.drummer}'s albums"
        context["drummer"] = self.drummer
        return context


class DrummerTracksView(ListView):
    model = Track
    template_name = "discography/drummer-tracks.html"
    context_object_name = "tracks"

    def get_queryset(self):
        self.drummer = get_object_or_404(Drummer, slug=self.kwargs["slug"])
        tracks = (
            Track.objects.filter(drummers=self.drummer)
            .prefetch_related("artists")
            .order_by("artists__name")
        )
        for track in tracks:
            track.video_id = get_video_id(track.track_url)
        return tracks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.drummer}'s tracks"
        context["drummer"] = self.drummer
        return context


def album_tracks(request, album_title, slug):
    drummer = get_object_or_404(Drummer, slug=slug)
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
                "discography:album_tracks",
                album_title=album.title,
                slug=drummer.slug,
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

    return render(request, "discography/album-tracks.html", context)
