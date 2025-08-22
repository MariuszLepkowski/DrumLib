from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls")),
    path("drummers/", include("drummers.urls")),
    path("discographies/", include("discography.urls")),
    path("admin/", admin.site.urls),
    path("album-generator/", include("album_generator.urls")),
    path("", include("user_management.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("comments/", include("comments.urls", namespace="comments")),
    path("suggestions/", include("suggestions.urls", namespace="suggestions")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
