from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            return redirect('tickets:history')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

@login_required
def ticket_history(request):
    tickets = Ticket.objects.filter(author=request.user)
    return render(request, 'tickets/history.html', {'tickets': tickets})

@login_required
def update_status(request, ticket_id, new_status):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.user == ticket.receiver:
        ticket.status = new_status
        ticket.save()
    return redirect('tickets:history')
