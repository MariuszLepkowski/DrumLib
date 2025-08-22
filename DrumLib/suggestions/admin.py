from django.contrib import admin

from .models import AlbumSuggestion, DrummerSuggestion


class DrummerSuggestionAdmin(admin.ModelAdmin):
    list_display = ("name", "suggested_by", "created_at", "is_reviewed")
    list_filter = ("is_reviewed",)
    actions = ["mark_as_reviewed"]

    def mark_as_reviewed(self, request, queryset):
        queryset.update(is_reviewed=True)

    mark_as_reviewed.short_description = "Mark selected suggestions as reviewed"


admin.site.register(DrummerSuggestion, DrummerSuggestionAdmin)


class AlbumSuggestionAdmin(admin.ModelAdmin):
    list_display = (
        "album_author",
        "album_title",
        "drummers_on_album",
        "suggested_by",
        "created_at",
        "is_reviewed",
    )
    list_filter = ("is_reviewed",)
    actions = ["mark_as_reviewed"]

    def mark_as_reviewed(self, request, queryset):
        queryset.update(is_reviewed=True)

    mark_as_reviewed.short_description = "Mark selected suggestions as reviewed"


admin.site.register(AlbumSuggestion, AlbumSuggestionAdmin)
