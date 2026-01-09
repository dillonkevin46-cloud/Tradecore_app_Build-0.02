from django.urls import path
from . import views

urlpatterns = [
    # Main Ticket Views
    path('', views.ticket_list, name='ticket_list'),
    path('archive/', views.ticket_archive, name='ticket_archive'),
    path('create/', views.create_ticket, name='ticket_create'), # <--- FIXED NAME
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('<int:pk>/edit/', views.ticket_edit, name='ticket_edit'),

    # Category Views
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
]