from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Ticket, TicketComment, Category
from .forms import TicketForm, CommentForm, CategoryForm

@login_required(login_url='/admin/login/')
def ticket_list(request):
    # Only show active tickets (exclude CLOSED)
    tickets = Ticket.objects.exclude(status='CLOSED').order_by('-created_at')
    
    # Stats
    open_count = Ticket.objects.filter(status='OPEN').count()
    resolved_count = Ticket.objects.filter(status='RESOLVED').count()
    closed_count = Ticket.objects.filter(status='CLOSED').count() # New stat for Archive
    
    context = {
        'tickets': tickets,
        'open_count': open_count,
        'resolved_count': resolved_count,
        'closed_count': closed_count
    }
    return render(request, 'tickets.html', context)

# 2. NEW: Archive List (Shows ONLY Closed Tickets)
@login_required(login_url='/admin/login/')
def ticket_archive(request):
    tickets = Ticket.objects.filter(status='CLOSED').order_by('-updated_at')
    return render(request, 'ticket_archive.html', {'tickets': tickets})

# 3. NEW: Edit Ticket
@login_required(login_url='/admin/login/')
def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket) # Load existing data
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk=ticket.id)
    else:
        form = TicketForm(instance=ticket) # Pre-fill form
        
    return render(request, 'ticket_edit.html', {'form': form, 'ticket': ticket})

@login_required(login_url='/admin/login/')
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

# --- NEW VIEW: TICKET DETAIL ---
@login_required(login_url='/admin/login/')
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    technicians = User.objects.filter(is_staff=True) # Get IT staff for dropdown

    # Handle Comment Submission
    if request.method == 'POST' and 'add_comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect('ticket_detail', pk=pk)
    else:
        comment_form = CommentForm()

    # Handle Status/Assign Updates
    if request.method == 'POST' and 'update_status' in request.POST:
        new_status = request.POST.get('status')
        new_tech_id = request.POST.get('assigned_to')
        
        if new_status:
            ticket.status = new_status
        if new_tech_id:
            ticket.assigned_to = User.objects.get(id=new_tech_id)
            
        ticket.save()
        return redirect('ticket_detail', pk=pk)

    context = {
        'ticket': ticket,
        'comment_form': comment_form,
        'technicians': technicians
    }
    return render(request, 'ticket_detail.html', context)

@login_required(login_url='/admin/login/')
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'category_list.html', {'categories': categories})

@login_required(login_url='/admin/login/')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

@login_required(login_url='/admin/login/')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})