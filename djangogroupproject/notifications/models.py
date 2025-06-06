from django.db import models

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE, blank=True, null=True)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)