from django.urls import path

from . import views

app_name = "suggestions_app"

urlpatterns = [
    path("", views.suggest_content, name="suggest_content"),
    path("drummer", views.suggest_drummer, name="suggest_drummer"),
    path("album", views.suggest_album, name="suggest_album"),
    path("thank-you", views.suggestions_thank_you, name="suggestions_thank_you"),
]
