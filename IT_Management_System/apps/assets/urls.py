from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('add/', views.asset_create, name='asset_create'),
    path('edit/<int:pk>/', views.asset_edit, name='asset_edit'),
    path('delete/<int:pk>/', views.asset_delete, name='asset_delete'),
    path('export/', views.asset_export, name='asset_export'),
    path('import/', views.asset_import, name='asset_import'),
    path('categories/', views.category_list, name='asset_category_list'),
    path('categories/delete/<int:pk>/', views.category_delete, name='asset_category_delete'),
]