from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()



class CampaignMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image','Image'),
        ('video', 'Video'),
        ('text', 'Text'),
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=8, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='campaign_media/', blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    caption = models.CharField(max_length=255, blank=True)

class Meta:
    ordering = ['order']