from django.contrib import admin
from .models import Campaign


# Register your models here.
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "status", "goal_amount")



