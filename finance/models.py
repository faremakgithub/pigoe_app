from django.conf import settings
from django.db import models

from core.models import Organization
from members.models import Member


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
