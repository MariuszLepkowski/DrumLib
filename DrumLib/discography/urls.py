from django.urls import path

from . import views

app_name = "discography"

urlpatterns = [
    path("", views.DrummersListView.as_view(), name="drummers_list"),
    path(
        "discographies/<slug:slug>/albums/",
        views.DrummerAlbumsView.as_view(),
        name="drummer_albums",
    ),
    path(
        "discographies/<slug:slug>/tracks/",
        views.DrummerTracksView.as_view(),
        name="drummer_tracks",
    ),
    path(
        "discographies/<slug:slug>/<album_title>/tracks/",
        views.AlbumTracksView.as_view(),
        name="album_tracks",
    ),
]
