from django import forms
from .models import Donation, RecurringDonation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('campaign', 'amount', 'currency', 'donor_name', 'is_anonymous')

class RecurringDonationForm(forms.ModelForm):
    class Meta:
        model = RecurringDonation
        fields = ('campaign', 'amount', 'currency', 'frequency')

