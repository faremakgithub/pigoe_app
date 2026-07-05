from django.core.management import call_command
from django.test import TestCase

from .models import Organization

PILOT_ORGANIZATION_NAME = (
    "Église des Assemblées de Dieu, Temple de la Grâce de Bassar Kpankissi"
)


class OrganizationModelTests(TestCase):
    def test_create_organization_with_defaults(self):
        org = Organization.objects.create(name="Église Test")

        self.assertEqual(org.country, "TG")
        self.assertEqual(org.timezone, "Africa/Lome")
        self.assertIsNotNone(org.created_at)

    def test_str_returns_name(self):
        org = Organization.objects.create(name="Église Test")

        self.assertEqual(str(org), "Église Test")


class SeedOrganizationCommandTests(TestCase):
    """Test de bout en bout — ADR-0011 : l'organisation pilote doit pouvoir
    être amorcée de façon fiable et idempotente sur une nouvelle instance."""

    def test_creates_pilot_organization(self):
        call_command("seed_organization")

        org = Organization.objects.get(name=PILOT_ORGANIZATION_NAME)
        self.assertEqual(org.country, "TG")
        self.assertEqual(org.timezone, "Africa/Lome")

    def test_running_twice_does_not_create_a_duplicate(self):
        call_command("seed_organization")
        call_command("seed_organization")

        self.assertEqual(
            Organization.objects.filter(name=PILOT_ORGANIZATION_NAME).count(), 1,
        )
