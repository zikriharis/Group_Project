from django import forms
from .models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'logo', 'description', 'website', 'address', 'contact_email')

