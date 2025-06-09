from django.shortcuts import render, redirect
from .forms import CampaignSubscriptionForm

def subscribe_campaign(request):
    if request.method == 'POST':
        form = CampaignSubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CampaignSubscriptionForm()
    return render(request, 'payments/subscribe.html', {'form': form})