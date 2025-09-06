from comments.forms import CommentForm
from comments.models import Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from drummers.models import Drummer

from .models import Album, Track
from .utils import get_video_id


class DrummersListView(ListView):
    """List of all drummers with discographies."""

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
    """Albums for a specific drummer."""

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
    """Tracks for a specific drummer."""

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


class AlbumTracksView(FormMixin, DetailView):
    """Tracks from a specific album + comments form."""

    model = Album
    template_name = "discography/album-tracks.html"
    context_object_name = "album"
    slug_field = "title"
    slug_url_kwarg = "album_title"
    form_class = CommentForm

    def get_object(self, queryset=None):
        self.drummer = get_object_or_404(Drummer, slug=self.kwargs["slug"])
        return get_object_or_404(
            Album, title=self.kwargs["album_title"], drummers=self.drummer
        )

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.album = self.object
            comment.drummer = self.drummer
            comment.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.object
        tracks = Track.objects.filter(albums=album, drummers=self.drummer)
        for track in tracks:
            track.video_id = get_video_id(track.track_url)
        context.update(
            {
                "title": album.title,
                "tracks": tracks,
                "artists": album.artists.all(),
                "drummer": self.drummer,
                "form": self.get_form(),
                "comments": Comment.objects.filter(album=album, drummer=self.drummer),
            }
        )
        return context
