from django.contrib import admin
from .models import CampaignSubscription

#NEED TO ADD START AND END DATE
@admin.register(CampaignSubscription)
class CampaignSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'organization', 'status', 'created_at', 'updated_at')