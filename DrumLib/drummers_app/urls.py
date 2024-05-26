from django.urls import path

from . import views

app_name = "drummers_app"

urlpatterns = [
    path("drummers/", views.drummers, name="drummers"),
    path("drummers/<drummer_name>/", views.drummer_profile, name="drummer_card"),
]