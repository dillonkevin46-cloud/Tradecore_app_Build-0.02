from django.urls import path
from . import views

urlpatterns = [
    path('', views.monitor_list, name='monitor_list'),
    path('add/', views.target_add, name='target_add'),
    path('edit/<int:pk>/', views.target_edit, name='target_edit'),
    path('delete/<int:pk>/', views.target_delete, name='target_delete'),
    
    # --- Categories ---
    path('categories/', views.monitor_category_list, name='monitor_category_list'),
    path('categories/add/', views.monitor_category_add, name='monitor_category_add'), # <--- NEW
    path('categories/delete/<int:pk>/', views.monitor_category_delete, name='monitor_category_delete'),
]