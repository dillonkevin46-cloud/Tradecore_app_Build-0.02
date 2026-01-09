from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from apps.tickets.models import Ticket, Category
from apps.assets.models import Asset
from apps.monitoring.models import NetworkTarget, MonitorCategory

@login_required(login_url='/login/')
def dashboard(request):
    # ==============================
    # 1. TICKET GRAPH DATA
    # ==============================
    # Fetch ALL tickets (or change .all() to .filter(status='OPEN') for active only)
    # We removed the date filter to ensure data shows up for testing.
    all_tickets = Ticket.objects.all()

    labels = []
    data = []

    # A. Loop through Ticket Categories
    ticket_categories = Category.objects.all()
    for cat in ticket_categories:
        count = all_tickets.filter(category=cat).count()
        if count > 0:
            labels.append(cat.name)
            data.append(count)
    
    # B. Handle "Uncategorized" Tickets
    uncategorized_count = all_tickets.filter(category__isnull=True).count()
    if uncategorized_count > 0:
        labels.append("Uncategorized")
        data.append(uncategorized_count)

    # ==============================
    # 2. MONITORING HEALTH LOGIC
    # ==============================
    monitor_stats = []
    
    # A. Loop through Defined Monitor Categories
    mon_cats = MonitorCategory.objects.all()
    for m_cat in mon_cats:
        devices = NetworkTarget.objects.filter(category=m_cat, is_active=True)
        offline_count = devices.filter(is_online=False).count()
        total_count = devices.count()
        
        if total_count == 0:
            status = "EMPTY"
            status_color = "secondary"
            message = "No devices assigned"
        elif offline_count > 0:
            status = "ERROR"
            status_color = "danger"
            message = f"{offline_count} / {total_count} Devices Offline"
        else:
            status = "HEALTHY"
            status_color = "success"
            message = f"All {total_count} Systems Operational"

        monitor_stats.append({
            'name': m_cat.name,
            'icon': m_cat.icon,
            'status': status,
            'color': status_color,
            'message': message
        })

    # B. Handle "Uncategorized" Monitors (Devices with NO Category)
    uncat_devices = NetworkTarget.objects.filter(category__isnull=True, is_active=True)
    if uncat_devices.exists():
        offline_uncat = uncat_devices.filter(is_online=False).count()
        total_uncat = uncat_devices.count()
        
        if offline_uncat > 0:
            u_status = "ERROR"
            u_color = "danger"
            u_msg = f"{offline_uncat} Uncategorized Devices Offline"
        else:
            u_status = "HEALTHY"
            u_color = "success"
            u_msg = f"{total_uncat} Uncategorized Devices OK"

        monitor_stats.append({
            'name': "General / Uncategorized",
            'icon': "fas fa-question-circle",
            'status': u_status,
            'color': u_color,
            'message': u_msg
        })

    context = {
        'chart_labels': labels,
        'chart_data': data,
        'monitor_stats': monitor_stats,
    }
    
    return render(request, 'dashboard.html', context)

def custom_logout(request):
    logout(request)
    return redirect('login')