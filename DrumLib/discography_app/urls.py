from django.urls import path
from . import views

app_name = 'discography_app'

urlpatterns = [
    path('', views.drummers_list, name='drummers_list'),
    path('<str:drummer_name>/albums/', views.drummer_albums, name='drummer_albums'),
    path('<str:drummer_name>/tracks/', views.drummer_tracks, name='drummer_tracks'),
    path('<str:album_title>/tracklist/<str:drummer_name>', views.album_tracks, name='album_tracks'),
]
