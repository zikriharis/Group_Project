from django.contrib import admin
from .models import Tag, CampaignTag

# Register your models here.
@admin.register(Tag)
class TagAdmin(Tag):
    list_display = ('name', 'category', 'slug')

@admin.register(CampaignTag)
class CampaignTagAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'tag')