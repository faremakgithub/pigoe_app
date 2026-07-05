from django.core.management.base import BaseCommand

from core.models import Organization


class Command(BaseCommand):
    """
    Initialise l'organisation pilote de PIGOE v1.

    Conformément à ADR-0011 (Architecture Vision) et ADR-0008 (priorisation
    du marché togolais), cette commande crée l'unique instance Organization
    du MVP — le multi-tenant restant différé (P8 du FEB).

    Usage : python manage.py seed_organization
    """

    help = "Crée l'organisation pilote PIGOE (Église des Assemblées de Dieu, Temple de la Grâce de Bassar Kpankissi)"

    def handle(self, *args, **options):
        org, created = Organization.objects.get_or_create(
            name="Église des Assemblées de Dieu, Temple de la Grâce de Bassar Kpankissi",
            defaults={"country": "TG", "timezone": "Africa/Lome"},
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Organisation pilote créée : {org.name}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Organisation pilote déjà existante : {org.name}")
            )
