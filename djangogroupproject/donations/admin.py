from django.contrib import admin
from .models import Donation, RecurringDonation, DonationBadge

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_display', 'amount', 'campaign', 'status', 'created_at']
    list_filter = ['status', 'is_anonymous', 'created_at']
    search_fields = ['donor_name', 'campaign__title']
    
    def donor_display(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return obj.donor_name or (obj.user.username if obj.user else "Guest")
    donor_display.short_description = "Donor"

@admin.register(RecurringDonation)
class RecurringDonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'campaign', 'amount', 'frequency', 'is_active']
    list_filter = ['frequency', 'is_active']

@admin.register(DonationBadge)
class DonationBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge_type', 'awarded_at']
    list_filter = ['badge_type']
