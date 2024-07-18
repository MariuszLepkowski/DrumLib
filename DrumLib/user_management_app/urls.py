from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, logout_view, CustomLoginView, profile

app_name = 'user_management_app'

urlpatterns = [
    path('register/', register, name='register'),
    path('accounts/login/', CustomLoginView.as_view(template_name='user_management_app/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user_management_app/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user_management_app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_management_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user_management_app/password_reset_complete.html'), name='password_reset_complete'),
]
