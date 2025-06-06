from django.contrib import admin
from .models import Campaign, CampaignPageBlock, CampaignDocument, Like, FraudReport

# Register your models here.
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'status', 'start_date', 'end_date', 'goal_amount', 'current_amount')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

@admin.register(CampaignPageBlock)
class CampaignPageBlockAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'block_type', 'sort_order')

@admin.register(CampaignDocument)
class CampaignDocumentAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'document', 'status', 'reviewed_by')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'created_at')

@admin.register(FraudReport)
class FraudReportAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'reporter', 'status', 'created_at')