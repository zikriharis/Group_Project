from django import forms
from .models import CampaignSubscription

class CampaignSubscriptionForm(forms.ModelForm):
    class Meta:
        model = CampaignSubscription
        fields = ('campaign', 'organization', 'payment_proof')