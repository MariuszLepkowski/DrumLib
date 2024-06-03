from django.contrib import admin

# Register your models here.

from .models import Album, Artist, Track


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Album, AuthorAdmin)
admin.site.register(Artist, AuthorAdmin)
admin.site.register(Track, AuthorAdmin)
