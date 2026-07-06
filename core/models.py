from django.conf import settings
from django.db import models


class Organization(models.Model):
    """
    Socle transverse — Business Architecture Chapitre 6.2.
    Prépare le multi-tenant (P8, différé) sans l'activer : une seule
    instance existe pour le MVP, mais toutes les autres entités y sont
    déjà rattachées via ForeignKey, garantissant une migration future
    sans réécriture (Architecture Vision, conformité P8).
    """

    name = models.CharField(max_length=200)
    country = models.CharField(max_length=2, default="TG")  # ISO 3166-1 alpha-2
    timezone = models.CharField(max_length=50, default="Africa/Lome")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def __str__(self):
        return self.name


class Church(models.Model):
    """Église / entité pastorale importée depuis la base pilote."""

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    legacy_id = models.BigIntegerField(null=True, blank=True, unique=True)
    hierarchy = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    annex_count = models.PositiveIntegerField(default=0)
    domain = models.CharField(max_length=255)
    member_count = models.PositiveIntegerField(default=0)
    founded_at = models.DateField(null=True, blank=True)
    photo_main = models.CharField(max_length=255, blank=True)
    photo_secondary = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_churches",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Église"
        verbose_name_plural = "Églises"
        ordering = ["name"]

    def __str__(self):
        return self.name
