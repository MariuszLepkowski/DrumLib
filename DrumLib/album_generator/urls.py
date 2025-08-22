from django.urls import path
from .views import album_generator_form, generate_random_album

app_name = 'album_generator_app'

urlpatterns = [
    path('', album_generator_form, name='album_generator_form'),
    path('generate/', generate_random_album, name='generate_random_album'),
]
