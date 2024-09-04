from django.urls import path
from . import views

app_name = "suggestions_app"

urlpatterns = [
    path('suggest/', views.suggest_content, name='suggest_content'),
    path('suggest/drummer', views.suggest_drummer, name='suggest_drummer'),
    path('suggest/album', views.suggest_album, name='suggest_album'),
]