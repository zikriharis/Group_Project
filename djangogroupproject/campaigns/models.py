import uuid
from django.db import models
from organizations.models import Organization
from users.models import User

# Create your models here.
class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='campaigns')
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    brief_description = models.CharField(max_length=500)
    main_image = models.ImageField(upload_to='campaign/main_images')
    country = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency_campaign = models.CharField(max_length=10, default='MYR')
    status = models.CharField(max_length=30, choices=(
        ('draft', 'Draft'),
        ('pending_main_approval', 'Pending Main Approval'),
        ('pending_page_approval', 'Pending Page Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('stopped', 'Stopped'),
        ('completed', 'Completed'),
    ), default='draft')
    external_link=models.URLField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('tags.Tag', through='tags.CampaignTag', blank=True)

def __str__(self):
    return self.title

class CampaignPageBlock(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='blocks')
    block_type = models.CharField(max_length=20, choices=(
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ))
    text_content = models.TextField(blank=True, null=True)
    media_file = models.FileField(upload_to='campaign/media/', blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

class Meta:
    ordering = ['sort_order']


