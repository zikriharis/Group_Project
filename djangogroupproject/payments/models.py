from django.db import models

# Create your models here.
class CampaignSubscription(models.Model):
    campaign = models.OneToOneField('campaigns.Campaign', on_delete=models.CASCADE, related_name='subscription')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=(
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ), default='pending')
    # Instead of manual, automatic confirmation need to be implemented later
    payment_proof = models.FileField(upload_to='subscriptions/payment_proof/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)