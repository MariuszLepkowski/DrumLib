from django.contrib import admin

from .models import Album, Artist, Track


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "artists",
        "drummers",
        "tracks",
    )
    list_display = (
        "title",
        "release_year",
        "genre",
        "album_url",
    )


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    filter_horizontal = ("collaborating_drummers",)
    list_display = ("name",)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "artists",
        "drummers",
    )
    list_display = (
        "title",
        "track_url",
    )
