from django.urls import path

from . import views

app_name = "drummers"

urlpatterns = [
    path("", views.drummers, name="drummers_list"),
    path("<drummer_name>/", views.drummer_profile, name="drummer_profile"),
]
