from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from .forms import CustomUserCreationForm, UserUpdateForm  # <--- Imported UserUpdateForm

@login_required(login_url='/login/')
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'user_list.html', {'users': users})

@login_required(login_url='/login/')
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_form.html', {'form': form, 'title': 'Create New User'})

@login_required(login_url='/login/')
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        # Use the form to handle validation and Groups saving automatically
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "User permissions and roles updated.")
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user_obj)

    return render(request, 'user_edit.html', {'form': form, 'user_obj': user_obj})

@login_required(login_url='/login/')
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, "User deleted.")
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user_obj': user_obj})

@login_required(login_url='/login/')
def user_password_reset(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = SetPasswordForm(user_obj, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Password for {user_obj.username} has been reset successfully.")
            return redirect('user_list')
    else:
        form = SetPasswordForm(user_obj)
    
    return render(request, 'user_password_reset.html', {
        'form': form, 
        'user_obj': user_obj
    })