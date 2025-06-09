from django import forms
from .models import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            'title',
            'description',
            'goal_amount',
            'end_date',
            'category',
            'image',
            'video_url',
            'tags',
        ]
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind CSS classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
            })


class CampaignAdminReviewForm(forms.ModelForm):
    ACTION_CHOICES = [
        ('approve', 'Approve Campaign'),
        ('reject', 'Reject Campaign'),
        # Potentially add 'request_more_info' if needed later
    ]
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.RadioSelect(attrs={'class': 'space-y-2'}), required=True)
    admin_remarks = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide feedback or reasons for your decision...'}),
        required=False, 
        label='Administrator Remarks'
    )

    class Meta:
        model = Campaign
        fields = ['admin_remarks'] # 'action' is handled separately

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind CSS classes to form fields
        self.fields['admin_remarks'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
        })
        # Style radio select labels if possible, or rely on template for styling
        # For radio buttons, Tailwind styling is often best applied in the template
