from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from core.models import Organization
from members.models import Member

from .models import Contribution


class ContributionModelTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Église Test")
        self.member = Member.objects.create(
            organization=self.org,
            first_name="Kodjo",
            last_name="Mensah",
            phone="+22890123456",
        )
        self.user = get_user_model().objects.create_user(
            username="admin", password="test-pass-123",
        )

    def test_create_contribution(self):
        contribution = Contribution.objects.create(
            organization=self.org,
            member=self.member,
            type=Contribution.Type.DUES,
            amount=Decimal("5000"),
            payment_method=Contribution.PaymentMethod.MOBILE_MONEY,
            created_by=self.user,
        )

        self.assertEqual(contribution.status, Contribution.Status.PENDING)
        self.assertEqual(contribution.amount, Decimal("5000"))

    def test_member_cannot_be_deleted_while_contributions_exist(self):
        # US-12 traçabilité : on_delete=PROTECT sur member
        Contribution.objects.create(
            organization=self.org,
            member=self.member,
            type=Contribution.Type.DONATION,
            amount=Decimal("1000"),
            payment_method=Contribution.PaymentMethod.CASH,
            created_by=self.user,
        )

        with self.assertRaises(ProtectedError):
            self.member.delete()
