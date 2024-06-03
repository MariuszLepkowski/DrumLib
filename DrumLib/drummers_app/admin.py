from django.contrib import admin

# Register your models here.

from .models import Drummer, DrummerPhoto


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Drummer, AuthorAdmin)
admin.site.register(DrummerPhoto, AuthorAdmin)
