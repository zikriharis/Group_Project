from django.db import models

# Create your models here.
class Campaign(models.Model):
    title = models.CharField(max_length=63)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='campaigns')
    slug = models.SlugField()
    text = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=16, choices=[('active', 'Active'),('completed', 'Completed')],default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    currency_campaign = models.CharField(max_length=10, default='MYR')
