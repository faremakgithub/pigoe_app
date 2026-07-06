from django.conf import settings
from django.db import models

from core.models import Church, Organization
from members.models import Member


class AccountPlan(models.Model):
    """Plan comptable importé depuis la base pilote."""

    class AccountType(models.TextChoices):
        DEBIT = "debit", "Débit"
        CREDIT = "credit", "Crédit"
        BOTH = "les_deux", "Les deux"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    church = models.ForeignKey(
        Church, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="account_plans",
    )
    legacy_id = models.BigIntegerField(null=True, blank=True, unique=True)
    title = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20, blank=True)
    account_type = models.CharField(
        max_length=10, choices=AccountType.choices, default=AccountType.BOTH,
    )
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="created_account_plans",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Plan comptable"
        verbose_name_plural = "Plans comptables"
        ordering = ["account_number"]

    def __str__(self):
        return f"{self.account_number} — {self.title}"


class LedgerEntry(models.Model):
    """Écriture financière importée depuis la base pilote."""

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    church = models.ForeignKey(
        Church, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="ledger_entries",
    )
    account_plan = models.ForeignKey(
        AccountPlan, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="ledger_entries",
    )
    legacy_id = models.BigIntegerField(null=True, blank=True, unique=True)
    debit = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    title = models.CharField(max_length=255, blank=True)
    operation_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    reference_number = models.CharField(max_length=50, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="created_ledger_entries",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Écriture comptable"
        verbose_name_plural = "Écritures comptables"
        ordering = ["-operation_date", "-created_at"]

    def __str__(self):
        amount = self.credit - self.debit
        return f"{self.title} — {amount} FCFA"


class Contribution(models.Model):
    """
    Transaction financière — US-07 à US-12.
    Le champ amount utilise DecimalField, jamais FloatField, pour
    éviter les erreurs d'arrondi sur des montants financiers — une
    exigence implicite de Security by Design (P18 du FEB).
    on_delete=PROTECT sur member et created_by : une fiche membre ou
    un compte utilisateur ne peuvent jamais être supprimés tant que des
    transactions financières y sont rattachées (traçabilité, US-12).
    """

    class Type(models.TextChoices):
        DUES = "dues", "Cotisation"
        DONATION = "donation", "Don"

    class PaymentMethod(models.TextChoices):
        MOBILE_MONEY = "mobile_money", "Mobile Money"
        CASH = "cash", "Espèces"

    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        CONFIRMED = "confirmed", "Confirmé"
        FAILED = "failed", "Échoué"
        CANCELLED = "cancelled", "Annulé"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    member = models.ForeignKey(
        Member, on_delete=models.PROTECT, related_name="contributions",
    )
    type = models.CharField(max_length=10, choices=Type.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=0)  # FCFA
    payment_method = models.CharField(
        max_length=15, choices=PaymentMethod.choices,
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING,
    )
    paydunya_token = models.CharField(max_length=100, blank=True)  # ADR-0014
    receipt_number = models.CharField(max_length=30, blank=True)  # US-07
    cancellation_reason = models.TextField(blank=True)  # US-07 traçabilité
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)  # US-12 journalisation

    class Meta:
        verbose_name = "Cotisation"
        verbose_name_plural = "Cotisations"
        indexes = [models.Index(fields=["member", "-created_at"])]  # US-10
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_type_display()} — {self.member} — {self.amount} FCFA"
