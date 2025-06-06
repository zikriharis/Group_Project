import uuid
from django.db import models

# Create your models here.
class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='org_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name