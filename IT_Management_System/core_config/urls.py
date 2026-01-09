from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.monitoring import views as monitor_views # For the dashboard home page

urlpatterns = [
    # --- ADMIN & AUTH ---
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # --- DASHBOARD (HOME) ---
    path('', monitor_views.dashboard, name='dashboard'),

    # --- APP URLS (Connecting the separate apps) ---
    path('assets/', include('apps.assets.urls')),
    path('monitor/', include('apps.monitoring.urls')),
    path('checklists/', include('apps.checklists.urls')),
    path('tickets/', include('apps.tickets.urls')),
    path('vault/', include('apps.vault.urls')),
    path('users/', include('apps.users.urls')),
]