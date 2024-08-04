from django.urls import path
from . import views

app_name = 'comments_app'

urlpatterns = [
    path('add/<str:content_type>/<int:object_id>/', views.add_comment, name='add_comment'),
]
