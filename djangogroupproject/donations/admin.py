from django.contrib import admin
from .models import Donation, RecurringDonation, DonationBadge

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'user', 'amount', 'currency', 'status', 'created_at')

@admin.register(RecurringDonation)
class RecurringDonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'user', 'amount', 'currency', 'frequency', 'is_active', 'created_at')

@admin.register(DonationBadge)
class DonationBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge_type', 'awarded_at')