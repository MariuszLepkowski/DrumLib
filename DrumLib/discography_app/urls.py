from django.urls import path
from . import views

app_name = 'discography_app'

urlpatterns = [
    path('discographies/', views.drummers_list, name='drummers_list'),
    path('discographies/<str:drummer_name>/albums/', views.drummer_albums, name='drummer_albums'),
    path('discographies/<str:drummer_name>/tracks/', views.drummer_tracks, name='drummer_tracks'),
]
