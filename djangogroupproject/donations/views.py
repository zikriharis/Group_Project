from django.shortcuts import render, redirect, get_object_or_404
from .forms import DonationForm, RecurringDonationForm
from ..campaigns.models import Campaign

# Create your views here.
def build_prefill_initial(request, campaign_id):
    initial = {'campaign': campaign_id}
    if request.user.is_authenticated:
        if request.user.first_name:
            initial['first_name'] = request.user.first_name
        if request.user.last_name:
            initial['last_name'] = request.user.last_name
        if request.user.email:
            initial['email'] = request.user.email
        # Add more user fields as needed
    return initial

def donate(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id) # defensive coding to validate the campaign exist
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if request.user.is_authenticated:
                donation.user = request.user
            donation.save()
            return redirect('campaign_detail', slug=donation.campaign.slug)
    else:
        # initial is used to pre-fill the form with default values
        initial = build_prefill_initial(request, campaign_id)
        form = DonationForm(initial=initial)
    return render(request, 'donations/donate.html', {'form': form})

def recurring_donation(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id) # defensive coding to validate the campaign exist
    if request.method == 'POST':
        form = RecurringDonationForm(request.POST)
        if form.is_valid():
            recurring = form.save(commit=False)
            if request.user.is_authenticated:
                recurring.user = request.user
            recurring.save()
            return redirect('campaign_detail', slug=recurring.campaign.slug)
    else:
        initial = build_prefill_initial(request, campaign_id)
        form = RecurringDonationForm(initial=initial)
    return render(request, 'donations/recurring.html', {'form': form})