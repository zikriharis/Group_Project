import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class Organization(models.Model):
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('verified', 'Verified'),
        ('declined', 'Declined'),
        ('needs_more_info', 'Needs More Information'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='org_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True)
    contact_email = models.EmailField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_organizations', on_delete=models.CASCADE, null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    legal_entity_details = models.TextField(help_text="Details about the organization's legal status, registration numbers, etc.", default='')
    admin_remarks = models.TextField(blank=True, help_text="Internal remarks by admin during verification.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrganisationApplicationDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, related_name='application_documents', on_delete=models.CASCADE)
    document = models.FileField(upload_to='organization_application_documents/')
    description = models.CharField(max_length=255, blank=True, help_text="Optional description of the document.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.organization.name} - {self.document.name}"