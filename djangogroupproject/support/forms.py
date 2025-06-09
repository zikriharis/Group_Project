from django import forms
from .models import HelpTopic, SupportTicket, ContactMessage

class HelpTopicForm(forms.ModelForm):
    class Meta:
        model = HelpTopic
        fields = ('question', 'answer')

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ('subject', 'message')

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'message')