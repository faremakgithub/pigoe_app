from django.core.validators import RegexValidator
from django.db import models

from core.models import Church, Organization

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

    class Sex(models.TextChoices):
        MASCULINE = "masculin", "Masculin"
        FEMININE = "feminin", "Féminin"

    class MaritalStatus(models.TextChoices):
        SINGLE = "celibataire", "Célibataire"
        MARRIED = "marie", "Marié(e)"
        DIVORCED = "divorce", "Divorcé(e)"
        WIDOWED = "veuf", "Veuf(ve)"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    church = models.ForeignKey(
        Church,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="members",
    )
    legacy_id = models.BigIntegerField(null=True, blank=True, unique=True)
    family = models.ForeignKey(
        Family, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="members",
    )
    membership_number = models.CharField(max_length=50, blank=True)
    has_left = models.BooleanField(default=False)
    is_deceased = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField(blank=True)
    sex = models.CharField(
        max_length=10, choices=Sex.choices, null=True, blank=True,
    )
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    profession = models.CharField(max_length=400, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    baptism_date = models.DateField(null=True, blank=True)
    baptism_place = models.CharField(max_length=100, blank=True)
    member_group = models.CharField(max_length=100, blank=True)
    conversion_date = models.DateField(null=True, blank=True)
    conversion_place = models.CharField(max_length=100, blank=True)
    holy_spirit_date = models.DateField(null=True, blank=True)
    holy_spirit_place = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(
        max_length=12, choices=MaritalStatus.choices,
        default=MaritalStatus.SINGLE,
    )
    children_count = models.PositiveIntegerField(null=True, blank=True)
    spouse = models.CharField(max_length=100, blank=True)
    guardian = models.CharField(max_length=100, blank=True)
    parent_contact = models.CharField(max_length=20, blank=True)
    activities = models.CharField(max_length=255, blank=True)
    member_type = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
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
