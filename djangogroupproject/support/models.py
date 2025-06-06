from django.db import models
from django.db.models import SET_NULL


# Create your models here.
class HelpTopic(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()


class SupportTicket(models.Model):
    user = models.ForeignKey("users.User", on_delete=SET_NULL, null=True, blank=True)  # for non-register user
    subject = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=(
            ("open", "Open"),
            ("closed", "Closed"),
            ("pending", "Pending"),
        ),
        default="open",
    )


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
