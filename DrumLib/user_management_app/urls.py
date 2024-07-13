from django.urls import path
from .views import register, logout_view
from django.contrib.auth import views as auth_views

app_name = 'user_management_app'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='user_management_app/login.html'),name='login'),
    path('logout/', logout_view, name='logout'),
]
