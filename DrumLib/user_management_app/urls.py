from django.urls import path
from .views import register

app_name = 'user_management_app'

urlpatterns = [
    path('register/', register, name='register'),
]