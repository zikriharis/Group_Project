import uuid
from django.db import models


# Create your models here.
class Donation(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="donations",
    )
    campaign = models.ForeignKey(
        "campaigns.Campaign", on_delete=models.CASCADE, related_name="donations"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency_donation = models.CharField(max_length=10, default="MYR")
    donor_name = models.CharField(max_length=255, blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    payment_reference = models.CharField(max_length=255, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        donor = self.donor_name or (self.user.username if self.user else "Anonymous")
        return f"{donor} - RM{self.amount} to {self.campaign.title}"


class RecurringDonation(models.Model):
    FREQUENCY_CHOICES = (  # ADD: Missing choices
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    )
        
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency_donation = models.CharField(max_length=10, default="MYR")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)  # add choices
    next_payment = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.frequency} RM{self.amount}"
    

class DonationBadge(models.Model):
    BADGE_CHOICES = (  # ADD: Missing choices
        ('first_donation', 'First Donation'),
        ('generous_donor', 'Generous Donor (RM1000+)'),
        ('loyal_supporter', 'Loyal Supporter (5+ donations)'),
        ('monthly_donor', 'Monthly Donor'),
        ('champion', 'Champion (RM5000+)'),
    )

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=50, choices=BADGE_CHOICES)  # Add badge here
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge_type')  # Prevent duplicate badges
    
    def __str__(self):
        return f"{self.user.username} - {self.get_badge_type_display()}"
