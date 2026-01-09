from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
import pandas as pd
from .models import Asset, AssetCategory
from .forms import AssetForm, AssetCategoryForm
from apps.monitoring.models import NetworkTarget, MonitorCategory

# --- HELPER: SYNC TO MONITOR ---
def sync_to_monitor(asset):
    """
    Syncs asset to monitoring system if 'is_monitored' is True.
    NOTE: Ideally, this should be moved to a Django Signal (post_save) 
    to decouple the apps.
    """
    if asset.is_monitored and asset.ip_address:
        try:
            # 1. Determine Category
            if asset.monitor_category:
                category = asset.monitor_category
            else:
                category, _ = MonitorCategory.objects.get_or_create(
                    name="Imported Assets", defaults={'icon': 'fas fa-laptop'}
                )

            # 2. Update or Create the Network Target
            NetworkTarget.objects.update_or_create(
                host=asset.ip_address,
                defaults={
                    'name': asset.device_name,
                    'category': category,
                    'is_active': True
                }
            )
        except Exception as e:
            # Log error but don't crash the asset save
            print(f"Monitor Sync Error: {e}")

# --- ASSET LIST & SEARCH ---
@login_required(login_url='/login/')
def asset_list(request):
    query = request.GET.get('q', '')
    cat_filter = request.GET.get('category', '')
    
    # Efficiently load related category to reduce DB queries
    assets = Asset.objects.select_related('category').all().order_by('category__name', 'device_name')
    categories = AssetCategory.objects.all()

    if query:
        assets = assets.filter(
            Q(device_name__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(ip_address__icontains=query) |
            Q(make__icontains=query) |
            Q(model__icontains=query) |
            Q(site__icontains=query)
        )
    
    if cat_filter:
        try:
            assets = assets.filter(category__id=int(cat_filter))
        except ValueError:
            pass

    context = {
        'assets': assets,
        'categories': categories,
        'query': query,
        'selected_cat': int(cat_filter) if cat_filter and cat_filter.isdigit() else None
    }
    return render(request, 'asset_list.html', context)

# --- CRUD OPERATIONS ---
@login_required(login_url='/login/')
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save()
            sync_to_monitor(asset)
            messages.success(request, "Asset created successfully.")
            return redirect('asset_list')
    else:
        form = AssetForm()
    return render(request, 'asset_form.html', {'form': form, 'title': 'Add New Asset'})

@login_required(login_url='/login/')
def asset_edit(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            sync_to_monitor(asset)
            messages.success(request, "Asset updated.")
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'asset_form.html', {'form': form, 'title': 'Edit Asset'})

@login_required(login_url='/login/')
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        asset.delete()
        messages.success(request, "Asset deleted.")
        return redirect('asset_list')
    return render(request, 'asset_confirm_delete.html', {'asset': asset})

# --- EXCEL EXPORT ---
@login_required(login_url='/login/')
def asset_export(request):
    assets = Asset.objects.all().values()
    if not assets:
        messages.warning(request, "No assets to export.")
        return redirect('asset_list')

    df = pd.DataFrame(list(assets))
    
    # Remove Timezones
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                df[col] = df[col].dt.tz_localize(None)
            except Exception:
                pass 

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="IT_Assets.xlsx"'
    df.to_excel(response, index=False)
    return response

# --- EXCEL IMPORT ---
@login_required(login_url='/login/')
def asset_import(request):
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        try:
            df = pd.read_excel(myfile)
            
            # Sanitize keys (lower case, strip spaces) to match logic
            df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

            count = 0
            for index, row in df.iterrows():
                serial = row.get('serial_number')
                
                # Skip if serial exists
                if serial and Asset.objects.filter(serial_number=serial).exists():
                    continue

                Asset.objects.create(
                    device_name=row.get('device_name', 'Unknown'),
                    make=row.get('make', ''),
                    model=row.get('model', ''),
                    serial_number=serial,
                    site=row.get('site', ''),
                    location=row.get('location', ''),
                    ip_address=row.get('ip_address', None),
                    cpu=row.get('cpu', ''),
                    ram=row.get('ram', ''),
                    storage=row.get('storage', ''),
                )
                count += 1
            
            messages.success(request, f"Successfully imported {count} assets.")
            return redirect('asset_list')
            
        except Exception as e:
            messages.error(request, f"Error importing file: {e}")
            
    return render(request, 'asset_import.html')

# --- CATEGORY MANAGEMENT ---
@login_required(login_url='/login/')
def category_list(request):
    categories = AssetCategory.objects.all()
    if request.method == 'POST':
        form = AssetCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added.")
            return redirect('asset_category_list') # Ensure this URL name matches urls.py
    else:
        form = AssetCategoryForm()
    return render(request, 'asset_category_list.html', {'categories': categories, 'form': form})

@login_required(login_url='/login/')
def category_delete(request, pk):
    cat = get_object_or_404(AssetCategory, pk=pk)
    cat.delete()
    messages.success(request, "Category deleted.")
    return redirect('asset_category_list')