from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
    
    # --- NEW PASSWORD RESET PATH ---
    path('reset-password/<int:pk>/', views.user_password_reset, name='user_password_reset'),
]