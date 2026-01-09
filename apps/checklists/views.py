from django.core.mail import send_mail
from django.conf import settings
from .models import ChecklistItem, DailyReport, ReportEntry, ReportRecipient # <--- Added ReportRecipient
from .forms import ChecklistItemForm, RecipientForm # <--- Added RecipientForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from .forms import ChecklistItemForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ChecklistItem, DailyReport, ReportEntry

@login_required(login_url='/login/')
def morning_check(request):
    items = ChecklistItem.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # 1. Create Report
        report = DailyReport.objects.create(
            technician=request.user,
            date=timezone.now().date(),
            notes=request.POST.get('general_notes', '')
        )
        
        # 2. Save Answers & Build Email Body
        email_body = f"Morning Check Report - {timezone.now().date()}\n"
        email_body += f"Technician: {request.user.first_name}\n\n"
        email_body += "--------------------------------------\n"
        
        has_failures = False

        for item in items:
            status = request.POST.get(f'status_{item.id}')
            comment = request.POST.get(f'comment_{item.id}', '')
            
            # Save to DB
            ReportEntry.objects.create(
                report=report, item=item, status=status, comment=comment
            )

            # Add to Email Text
            icon = "✅" if status == 'PASS' else "⚠️" if status == 'WARNING' else "❌"
            email_body += f"{icon} {item.name}: {status}\n"
            if comment:
                email_body += f"   Note: {comment}\n"
            
            if status == 'FAIL':
                has_failures = True
        
        email_body += "--------------------------------------\n"
        email_body += f"General Notes: {report.notes}\n"

        # 3. SEND EMAIL
        # Get active recipients
        recipients = list(ReportRecipient.objects.filter(is_active=True).values_list('email', flat=True))
        
        if recipients:
            subject_prefix = "[URGENT] ❌" if has_failures else "✅"
            subject = f"{subject_prefix} IT Morning Check: {timezone.now().date()}"
            
            try:
                send_mail(
                    subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    recipients,
                    fail_silently=False,
                )
                messages.success(request, "Report submitted and email sent!")
            except Exception as e:
                messages.warning(request, f"Report saved, but email failed: {e}")
        else:
            messages.info(request, "Report saved (No email recipients configured).")

        return redirect('dashboard')

    return render(request, 'morning_check.html', {'items': items})

def is_manager(user):
    return user.is_staff or user.is_superuser

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def checklist_setup(request):
    items = ChecklistItem.objects.all().order_by('-is_active', 'name')
    return render(request, 'checklist_setup.html', {'items': items})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def item_create(request):
    if request.method == 'POST':
        form = ChecklistItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New checklist item added.")
            return redirect('checklist_setup')
    else:
        form = ChecklistItemForm()
    return render(request, 'item_form.html', {'form': form, 'title': 'Add Checklist Item'})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def item_edit(request, pk):
    item = get_object_or_404(ChecklistItem, pk=pk)
    if request.method == 'POST':
        form = ChecklistItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Checklist item updated.")
            return redirect('checklist_setup')
    else:
        form = ChecklistItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form, 'title': 'Edit Item'})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def item_delete(request, pk):
    item = get_object_or_404(ChecklistItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted.")
        return redirect('checklist_setup')
    return render(request, 'item_confirm_delete.html', {'item': item})

# --- EMAIL RECIPIENT MANAGEMENT ---
@login_required(login_url='/login/')
@user_passes_test(is_manager)
def recipient_list(request):
    recipients = ReportRecipient.objects.all().order_by('-is_active', 'name')
    return render(request, 'recipient_list.html', {'recipients': recipients})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def recipient_add(request):
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipient added successfully.")
            return redirect('recipient_list')
    else:
        form = RecipientForm()
    return render(request, 'recipient_form.html', {'form': form})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def recipient_delete(request, pk):
    recipient = get_object_or_404(ReportRecipient, pk=pk)
    if request.method == 'POST':
        recipient.delete()
        messages.success(request, "Recipient removed.")
        return redirect('recipient_list')
    return render(request, 'recipient_confirm_delete.html', {'recipient': recipient})