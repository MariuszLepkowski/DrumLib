from django.urls import path
from .views import register, logout_view, CustomLoginView, profile

app_name = 'user_management_app'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='user_management_app/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
]
