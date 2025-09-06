from django.urls import path

from . import views

app_name = "discography"

urlpatterns = [
    path("", views.DrummerListView.as_view(), name="drummers_list"),
    path(
        "discographies/<slug:slug>/albums/",
        views.DrummerAlbumsView.as_view(),
        name="drummer_albums",
    ),
    path(
        "discographies/<slug:slug>/tracks/", views.drummer_tracks, name="drummer_tracks"
    ),
    path(
        "discographies/<slug:slug>/<album_title>/tracks/",
        views.album_tracks,
        name="album_tracks",
    ),
]
