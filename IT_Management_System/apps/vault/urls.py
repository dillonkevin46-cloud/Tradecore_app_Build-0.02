from django.urls import path
from . import views

urlpatterns = [
    path('', views.vault_list, name='vault_list'),
    path('add/', views.vault_add, name='vault_add'),
    path('reveal/<int:pk>/', views.vault_reveal, name='vault_reveal'),
    path('delete/<int:pk>/', views.vault_delete, name='vault_delete'),
]