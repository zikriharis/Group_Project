import uuid
from django.db import models

# Create your models here.
class Campaign(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending_main_approval', 'Pending Main Approval'),
        ('pending_page_approval', 'Pending Page Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('stopped', 'Stopped'),
        ('completed', 'Completed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    brief_description = models.CharField(max_length=500)
    main_image = models.ImageField(upload_to='campaign/main_images/')
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency_campaign = models.CharField(max_length=10, default='MYR')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    external_link=models.URLField(blank=True, null=True)
    org_external_link = models.URLField(blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('tags.Tag', through='tags.CampaignTag', blank=True)

    # Admin track campaigns setup request
    main_request_reviewed = models.BooleanField(default=False)
    page_request_reviewed = models.BooleanField(default=False)
    main_approved_by = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='main_approved_campaigns'
    )
    page_approved_by = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='page_approved_campaigns'
    )
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class CampaignPageBlock(models.Model):
    BLOCK_TYPE = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    )
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='blocks')
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPE)
    text_content = models.TextField(blank=True, null=True)
    media_file = models.FileField(upload_to='campaign/media/', blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']

class CampaignDocument(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='campaigns/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, choices=(
        ('pending','Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')
    reviewed_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL)
    rejection_reason = models.TextField(blank=True, null=True)

class Like(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'campaign')

class FraudReport (models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('action_taken', 'Action Taken'),
        ('rejected', 'Rejected'),
    )
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='fraud_reports')
    reporter = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='fraud_reports')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        'users.User',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_fraud_reports'
    )
    action_details = models.TextField(blank=True, null=True)