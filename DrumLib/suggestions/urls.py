from django.urls import path

from . import views

app_name = "suggestions"

urlpatterns = [
    path("", views.SuggestContentView.as_view(), name="suggest_content"),
    path("drummer/", views.SuggestDrummerView.as_view(), name="suggest_drummer"),
    path("album/", views.SuggestAlbumView.as_view(), name="suggest_album"),
    path(
        "thank-you/",
        views.SuggestionsThankYouView.as_view(),
        name="suggestions_thank_you",
    ),
]
