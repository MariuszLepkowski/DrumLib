from django.urls import path

from . import views

app_name = "drummers_app"

urlpatterns = [
    path("drummers/", views.drummers, name="drummers_list"),
    path("drummers/<drummer_name>/", views.drummer_profile, name="drummer_profile"),
    path("drummers/add-drummer", views.add_drummer, name="drummers"),
]