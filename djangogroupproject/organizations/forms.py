from django import forms
from .models import Organization, OrganisationApplicationDocument

class OrganizationApplicationForm(forms.ModelForm):
    # Field for uploading multiple documents, not directly tied to a single model field
    application_documents = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,  # Documents might be optional depending on final requirements
        help_text='Upload supporting documents (e.g., proof of registration, tax exemption).'
    )

    class Meta:
        model = Organization
        fields = [
            'name',
            'contact_email',
            'website',
            'description',
            'address',
            'legal_entity_details',
            # 'logo' can be added later or handled as part of org profile editing after verification
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Legal Name of Organization'}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'Official Contact Email'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Briefly describe your organization\'s mission and activities.'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Full Mailing Address'}),
            'legal_entity_details': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Provide legal entity details, registration numbers, etc. This information is required for verification.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['legal_entity_details'].required = True # Ensure it's required at form level
        self.fields['name'].required = True
        self.fields['contact_email'].required = True

    def save_documents(self, organization_instance):
        # This method will be called from the view after the Organization instance is saved
        for f in self.cleaned_data.get('application_documents', []):
            if f: # Ensure file is present
                OrganisationApplicationDocument.objects.create(
                    organization=organization_instance,
                    document=f
                )


class OrganizationAdminReviewForm(forms.ModelForm):
    # Exclude 'pending' as it's not an action an admin takes, but an initial state.
    ACTION_CHOICES = [
        ('', '---------'), # Default empty choice
        ('verified', 'Verify Application'),
        ('declined', 'Decline Application'),
        ('needs_more_info', 'Request More Information'),
    ]

    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        required=True,
        label="Review Action",
        help_text="Select an action to take for this application.",
        widget=forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
    )

    class Meta:
        model = Organization
        fields = ['admin_remarks'] # Only admin_remarks is directly from the model for this form
        widgets = {
            'admin_remarks': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide internal remarks or reasons for the decision. This will be visible to other admins.', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If remarks should be conditionally required, logic can be added here.
        # For example, if action is 'declined' or 'needs_more_info', make 'admin_remarks' required.
        # self.fields['admin_remarks'].required = False # Default, can be overridden
        pass

    def save(self, commit=True):
        organization = super().save(commit=False) # Get the organization instance without saving to DB yet
        
        selected_action = self.cleaned_data.get('action')
        if selected_action:
            organization.verification_status = selected_action
        
        # admin_remarks are already handled by ModelForm saving if field is in Meta.fields

        if commit:
            organization.save()
        return organization
