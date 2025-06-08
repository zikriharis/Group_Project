from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def make_donation(request, campaign_id):
    return HttpResponse(f"Donation page for campaign: {campaign_id}")


def donation_success(request, donation_id):
    return HttpResponse(f"Thank you! Donation {donation_id} successful!")


def my_donations(request):
    return HttpResponse("My donations page - coming soon!")


def manage_recurring(request):
    return HttpResponse("Manage recurring donations - coming soon!")
