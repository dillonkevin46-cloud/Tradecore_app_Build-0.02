from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import PasswordEntry  # <--- Updated Import
from .forms import PasswordEntryForm

# Security check: Only Superusers or Managers should see passwords
def is_manager(user):
    return user.is_superuser or user.groups.filter(name='Managers').exists()

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def vault_list(request):
    query = request.GET.get('q', '')
    entries = PasswordEntry.objects.all().order_by('title')
    
    # Filter if search term exists
    if query:
        entries = entries.filter(
            Q(title__icontains=query) | 
            Q(username__icontains=query) |
            Q(notes__icontains=query)
        )
    
    return render(request, 'vault_list.html', {'entries': entries, 'query': query})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def vault_add(request):
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            # Manually handle the password encryption
            raw_password = form.cleaned_data['password_input']
            if raw_password:
                entry.set_password(raw_password)
            entry.save()
            messages.success(request, "Password saved securely.")
            return redirect('vault_list')
    else:
        form = PasswordEntryForm()
    return render(request, 'vault_form.html', {'form': form, 'title': 'Add Password'})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def vault_delete(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Entry deleted.")
        return redirect('vault_list')
    return render(request, 'vault_confirm_delete.html', {'entry': entry})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def vault_reveal(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk)
    
    # 1. Attempt Decryption
    decrypted_password = entry.get_password()
    
    # 2. Check for Failure
    if decrypted_password is None:
        messages.error(request, "Error: Could not decrypt password. The Encryption Key may have changed.")
        decrypted_password = "[[ DECRYPTION FAILED ]]"

    return render(request, 'vault_reveal.html', {'entry': entry, 'password': decrypted_password})