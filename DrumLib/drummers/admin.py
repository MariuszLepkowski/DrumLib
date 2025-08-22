from django.contrib import admin
from .models import Drummer, DrummerPhoto


@admin.register(Drummer)
class DrummerAdmin(admin.ModelAdmin):
    filter_horizontal = ('photos', 'collaborating_artists')
    list_display = ('name', 'birth_date', 'death_date', 'nationality')

@admin.register(DrummerPhoto)
class DrummerPhotoAdmin(admin.ModelAdmin):
    filter_horizontal = ('drummers',)
    list_display = ('source', 'image_author')

