from django.urls import path
from . import views

urlpatterns = [
    # Main Checklist Page (View function is 'morning_check')
    path('', views.morning_check, name='daily_checklist'),

    # Checklist Setup (Manager Only)
    path('setup/', views.checklist_setup, name='checklist_setup'),
    path('setup/add/', views.item_create, name='item_create'),
    path('setup/edit/<int:pk>/', views.item_edit, name='item_edit'),
    path('setup/delete/<int:pk>/', views.item_delete, name='item_delete'),

    # Email Recipients
    path('recipients/', views.recipient_list, name='recipient_list'),
    path('recipients/add/', views.recipient_add, name='recipient_add'),
    path('recipients/delete/<int:pk>/', views.recipient_delete, name='recipient_delete'),
]