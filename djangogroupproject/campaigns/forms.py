from django import forms
from.models import Campaign, CampaignPageBlock, CampaignDocument, FraudReport, Like

'''
Think of a ModelForm like a user-facing form at the front desk of a system — it lets people submit or edit data, 
but the data still goes into the main database model.
It lets you interact with an existing model through form inputs.
'''

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('slug',
                  'organization',
                  'title',
                  'brief_description',
                  'main_image',
                  'country',
                  'start_date',
                  'end_date',
                  'goal_amount',
                  'currency',
                  'external_link',
                  'org_external_link',
                  'tags') # category?

class CampaignPageBlockForm(forms.ModelForm):
    class Meta:
        model = CampaignPageBlock
        fields = ('block_type', 'text_content', 'media_file', 'sort_order')

class CampaignDocumentForm(forms.ModelForm):
    class Meta:
        model = CampaignDocument
        fields = ('document', 'description')

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ('campaign',)

class FraudReportForm(forms.ModelForm):
    class Meta:
        model = FraudReport
        fields = ('campaign', 'reason')