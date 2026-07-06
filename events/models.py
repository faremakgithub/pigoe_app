from django.db import models

from core.models import Church, Organization
from members.models import Member


class EventType(models.Model):
    """Type d'événement importé depuis la base pilote."""

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    legacy_id = models.BigIntegerField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Type d'événement"
        verbose_name_plural = "Types d'événements"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    """Événement organisationnel — US-13, US-14."""

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    church = models.ForeignKey(
        Church, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="events",
    )
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="events",
    )
    legacy_id = models.BigIntegerField(null=True, blank=True, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    start_at = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)  # US-13
    reminder_hours_before = models.PositiveIntegerField(default=24)  # US-14
    reminder_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ["start_at"]

    def __str__(self):
        return self.title


class Attendance(models.Model):
    """Pointage de présence — US-15, US-16."""

    class Role(models.TextChoices):
        PRINCIPAL = "Principal", "Principal"
        TEMOIN = "Témoin", "Témoin"
        PARTICIPANT = "Participant", "Participant"
        AUTRE = "Autre", "Autre"

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="attendances",
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)  # US-15
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.PARTICIPANT,
    )
    note = models.TextField(blank=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Présence"
        verbose_name_plural = "Présences"
        unique_together = [["event", "member"]]

    def __str__(self):
        status = "présent" if self.present else "absent"
        return f"{self.member} — {self.event} ({status})"
