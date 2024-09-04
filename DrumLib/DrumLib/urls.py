"""
URL configuration for DrumLib project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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

