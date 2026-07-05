from django.core.validators import RegexValidator
from django.db import models

from core.models import Organization

phone_validator = RegexValidator(
    regex=r"^\+228\d{8}$",
    message="Le numéro doit être au format togolais : +228XXXXXXXX (US-01).",
)


class Family(models.Model):
    """Regroupement familial — US-05."""

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # ex. "Famille Mensah"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Famille"
        verbose_name_plural = "Familles"

    def __str__(self):
        return self.name


class Member(models.Model):
    """
    Fiche membre — US-01 à US-06.
    Le couple (organization, phone) est unique pour appuyer la
    détection de doublon de US-03 dès la couche base de données.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Actif"
        INACTIVE = "inactive", "Inactif"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    family = models.ForeignKey(
        Family, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="members",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField(blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # P11 Data by Design

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        indexes = [models.Index(fields=["phone"])]  # US-03 détection doublon
        unique_together = [["organization", "phone"]]
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
