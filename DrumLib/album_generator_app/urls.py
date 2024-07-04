from django.urls import path
from . import views

app_name = 'album_generator_app'


urlpatterns = [
    path('', views.random_album, name='random_album'),
]