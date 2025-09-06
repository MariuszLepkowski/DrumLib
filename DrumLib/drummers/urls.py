from django.urls import path

from .views import DrummerDetailView, DrummerListView

app_name = "drummers"

urlpatterns = [
    path("", DrummerListView.as_view(), name="drummer_list"),
    path("<slug>/", DrummerDetailView.as_view(), name="drummer_profile"),
]
