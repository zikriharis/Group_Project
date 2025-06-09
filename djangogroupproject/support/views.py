from django.shortcuts import render, redirect
from .forms import SupportTicketForm, ContactMessageForm
from .models import HelpTopic, SupportTicket

def help_list(request):
    help_topics = HelpTopic.objects.all()
    return render(request, 'support/help_list.html', {'help_topics': help_topics})

def create_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('help_list')
    else:
        form = SupportTicketForm()
    return render(request, 'support/ticket_form.html', {'form': form})

def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            # Maybe show a thank you page
    else:
        form = ContactMessageForm()
    return render(request, 'support/contact_form.html', {'form': form})