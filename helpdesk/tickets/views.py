from django.shortcuts import render, redirect
from .forms import CreateTicketForm
from django.contrib.auth.decorators import login_required
from .models import Ticket, Message
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models import Q
# Create your views here.

UNASSIGNED_STATUS = 1
PENDING_STATUS = 2
RESOLVED_STATUS = 3

@login_required(login_url='/user/login/')
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(data=request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user.email
            ticket.status = UNASSIGNED_STATUS
            ticket.save()
            message = Message(ticket=ticket, message=ticket.description, published_by='user', published_at=now())
            message.save()
            return redirect('list_tickets')
    else:
        form = CreateTicketForm()
        args = {'form' : form}
        return render(request, 'tickets/create_ticket.html', args)

@login_required(login_url='/user/login/')
def list_tickets(request):

    tickets = Ticket.objects.order_by('-created_on')
    status = request.GET.get('status')

    if request.user.is_staff:
        if request.user.department == 1:
            tickets = tickets.filter(department=1)
        elif request.user.department == 2:
            tickets = tickets.filter(department=2)
        elif request.user.department == 3:
            tickets = tickets.filter(department=3)
        else:
            tickets = tickets.filter(department=4)

        if status == 'unassigned':
            tickets = tickets.filter(status=1)
        elif status == 'pending':
            tickets = tickets.filter(status=2, accepted_by=request.user.email)
        elif status == 'resolved':
            tickets = tickets.filter(status=3, accepted_by=request.user.email)
        else:
            tickets = tickets.filter(Q(accepted_by__isnull=True) | Q(accepted_by=request.user.email))

        return render(request, 'tickets/list_tickets_agent.html', {'tickets' : tickets})
    else:
        if status == 'unassigned':
            tickets = tickets.filter(status=1)
        elif status == 'pending':
            tickets = tickets.filter(status=2)
        elif status == 'resolved':
            tickets = tickets.filter(status=3)
        tickets = tickets.filter(created_by=request.user.email)
        return render(request, 'tickets/list_tickets_user.html', {'tickets' : tickets})

@login_required(login_url='/user/login/')
def accept_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.accepted_by = request.user.email
    ticket.status = PENDING_STATUS
    ticket.save()
    return redirect('list_tickets')

@login_required(login_url='/user/login/')
def ticket_resolved(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.status = RESOLVED_STATUS
    ticket.save()
    return redirect('list_tickets')

@login_required(login_url='/user/login/')
def ticket_close(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.delete()
    return redirect('list_tickets')

@login_required(login_url='/user/login/')
def ticket_details(request, id):
    ticket= Ticket.objects.get(id=id)
    if request.method == 'POST':
        message = request.POST.get('message')
        if request.user.is_staff:
            messages = Message.objects.create(ticket=ticket, message=message, published_by='agent', published_at=now())
        else:
            messages = Message.objects.create(ticket=ticket, message=message, published_by='user', published_at=now())
        messages.save()
    messages = Message.objects.filter(ticket=ticket)
    messages = messages.order_by('published_at')
    user = get_user_model().objects.get(email=ticket.created_by)
    if ticket.accepted_by:
        agent = get_user_model().objects.get(email =ticket.accepted_by)
    else:
        agent = None
    return render(request, 'tickets/ticket_details.html', {'messages' : messages, 'created_by':user, 'accepted_by':agent})
