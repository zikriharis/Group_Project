from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from djangogroupproject.campaigns.models import Campaign

class CampaignListView(LoginRequiredMixin, ListView):
    """
    Campaign list page, only accessible for logged-in users.
    """
    model = Campaign
    template_name = 'campaigns/campaign_list.html'
    context_object_name = 'campaigns'