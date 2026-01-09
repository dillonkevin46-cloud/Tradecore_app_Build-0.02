from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import NetworkTarget, MonitorCategory
from .forms import NetworkTargetForm, MonitorCategoryForm
from apps.assets.models import Asset
from apps.vault.models import PasswordEntry

# --- DASHBOARD (HOME) ---
@login_required(login_url='/login/')
def dashboard(request):
    context = {
        'total_assets': Asset.objects.count(),
        'total_passwords': PasswordEntry.objects.count(),
        # Count ACTIVE monitors
        'active_monitors': NetworkTarget.objects.filter(is_active=True).count(),
        # Count TOTAL monitors (for debugging)
        'total_monitors': NetworkTarget.objects.count(), 
    }
    return render(request, 'dashboard.html', context)

# --- MONITORING ---
@login_required(login_url='/login/')
def monitor_list(request):
    categories_stats = MonitorCategory.objects.annotate(
        total=Count('networktarget', filter=Q(networktarget__is_active=True)),
        offline=Count('networktarget', filter=Q(networktarget__is_active=True, networktarget__is_online=False))
    )
    monitor_groups = {}
    for cat in MonitorCategory.objects.all():
        targets = NetworkTarget.objects.filter(category=cat, is_active=True).order_by('name')
        if targets.exists():
            monitor_groups[cat] = targets
            
    uncategorized = NetworkTarget.objects.filter(category__isnull=True, is_active=True)
    if uncategorized.exists():
        fake_cat = type('obj', (object,), {'name': 'Uncategorized', 'icon': 'fas fa-question-circle'})
        monitor_groups[fake_cat] = uncategorized

    return render(request, 'monitor_list.html', {
        'categories_stats': categories_stats,
        'monitor_groups': monitor_groups,
    })

# --- TARGET CRUD ---
@login_required(login_url='/login/')
def target_add(request):
    if request.method == 'POST':
        form = NetworkTargetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Device added.")
            return redirect('monitor_list')
    else:
        form = NetworkTargetForm()
    return render(request, 'target_form.html', {'form': form, 'title': 'Add Device'})

@login_required(login_url='/login/')
def target_edit(request, pk):
    target = get_object_or_404(NetworkTarget, pk=pk)
    if request.method == 'POST':
        form = NetworkTargetForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            messages.success(request, "Device updated.")
            return redirect('monitor_list')
    else:
        form = NetworkTargetForm(instance=target)
    return render(request, 'target_form.html', {'form': form, 'title': 'Edit Device'})

@login_required(login_url='/login/')
def target_delete(request, pk):
    target = get_object_or_404(NetworkTarget, pk=pk)
    target.delete()
    messages.success(request, "Device removed.")
    return redirect('monitor_list')

# --- CATEGORY MANAGEMENT ---
@login_required(login_url='/login/')
def monitor_category_list(request):
    """Lists categories only. Add logic moved to monitor_category_add."""
    categories = MonitorCategory.objects.all()
    return render(request, 'monitor_category_list.html', {'categories': categories})

@login_required(login_url='/login/')
def monitor_category_add(request):
    """Handles adding a new category on a separate page."""
    if request.method == 'POST':
        form = MonitorCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created.")
            return redirect('monitor_category_list')
    else:
        form = MonitorCategoryForm()
    # Using monitor_category_form.html (assuming it exists based on naming convention)
    # If not, use 'target_form.html' or create 'monitor_category_form.html'
    return render(request, 'monitor_category_form.html', {'form': form, 'title': 'Add Category'})

@login_required(login_url='/login/')
def monitor_category_delete(request, pk):
    cat = get_object_or_404(MonitorCategory, pk=pk)
    cat.delete()
    messages.success(request, "Category deleted.")
    return redirect('monitor_category_list')