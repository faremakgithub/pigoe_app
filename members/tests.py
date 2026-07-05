from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from core.models import Organization

from .models import Family, Member


class FamilyModelTests(TestCase):
    def test_str_returns_name(self):
        org = Organization.objects.create(name="Église Test")
        family = Family.objects.create(organization=org, name="Famille Mensah")

        self.assertEqual(str(family), "Famille Mensah")


class MemberModelTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Église Test")

    def test_full_name_property(self):
        member = Member.objects.create(
            organization=self.org,
            first_name="Kodjo",
            last_name="Mensah",
            phone="+22890123456",
        )

        self.assertEqual(member.full_name, "Kodjo Mensah")
        self.assertEqual(member.status, Member.Status.ACTIVE)

    def test_phone_format_is_validated(self):
        member = Member(
            organization=self.org,
            first_name="Kodjo",
            last_name="Mensah",
            phone="0123456789",  # format invalide (US-01)
        )

        with self.assertRaises(ValidationError):
            member.full_clean()

    def test_duplicate_phone_in_same_organization_is_rejected(self):
        # US-03 : détection de doublon au niveau base de données
        Member.objects.create(
            organization=self.org,
            first_name="Kodjo",
            last_name="Mensah",
            phone="+22890123456",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Member.objects.create(
                    organization=self.org,
                    first_name="Autre",
                    last_name="Personne",
                    phone="+22890123456",
                )
