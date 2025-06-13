from django.contrib import admin
from .models import Donation, RecurringDonation, DonationBadge

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'user', 'amount', 'currency_donation', 'status', 'created_at')

@admin.register(RecurringDonation)
class RecurringDonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'user', 'amount', 'currency_donation', 'frequency', 'is_active', 'created_at')

@admin.register(DonationBadge)
class DonationBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge_type', 'awarded_at')