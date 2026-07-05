from django.conf import settings
from django.db import models

from core.models import Organization
from members.models import Family


class Announcement(models.Model):
    """Annonce et message groupé — US-17 à US-20."""

    class Channel(models.TextChoices):
        SMS = "sms", "SMS"
        APP = "app", "Notification application"
        BOTH = "both", "SMS et application"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.CharField(max_length=160)  # US-17 contrainte SMS
    channel = models.CharField(max_length=10, choices=Channel.choices)
    target_family = models.ForeignKey(
        Family, null=True, blank=True, on_delete=models.SET_NULL,
    )
    scheduled_at = models.DateTimeField(null=True, blank=True)  # US-20
    sent_at = models.DateTimeField(null=True, blank=True)
    recipient_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
