from django import forms
from .models import User, Profile, CampaignManagerAssignment

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'country')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'bio')

class CampaignManagerAssignmentForm(forms.ModelForm):
    class Meta:
        model = CampaignManagerAssignment
        fields = ('user', 'campaign', 'organization')