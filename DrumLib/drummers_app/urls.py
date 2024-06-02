from django.urls import path

from . import views

app_name = "drummers_app"

urlpatterns = [
    path("", views.drummers, name="drummers_list"),
    path("<drummer_name>/", views.drummer_profile, name="drummer_profile"),
    path("add-drummer", views.add_drummer, name="add_drummer"),
]