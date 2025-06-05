from django.db import models

# Create your models here.
class Donation(models.Model):
    user = models.ForeignKey('users.user', on_delete=models.CASCADE, related_name= 'donations')
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    currency_donation = models.CharField(max_length=10, default='MYR')
    created_at = models.DateTimeField(auto_now_add=True)