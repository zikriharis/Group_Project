from django.db import models

# Create your models here.
class Tag(models.Model):
    CATEGORY_CHOICES = (
        ('cause', 'Cause Type'),
        #('region', 'Region'),
        ('country', 'Country'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64, choices = CATEGORY_CHOICES)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class CampaignTag(models.Model):
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('campaign', 'tag')