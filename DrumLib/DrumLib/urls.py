from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("home_app.urls")),
    path("drummers/", include("drummers_app.urls")),
    path('discographies/', include('discography_app.urls')),
    path('admin/', admin.site.urls),
    path('album-generator/', include('album_generator_app.urls')),
    path('', include('user_management_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('comments/', include('comments_app.urls', namespace='comments_app')),
    path('suggestions/', include('suggestions_app.urls', namespace='suggestions_app')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

