from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Organization

from .models import Announcement


class AnnouncementModelTests(TestCase):
    def test_create_announcement(self):
        org = Organization.objects.create(name="Église Test")
        user = get_user_model().objects.create_user(
            username="admin", password="test-pass-123",
        )

        announcement = Announcement.objects.create(
            organization=org,
            title="Réunion de prière",
            message="Réunion ce vendredi à 18h.",
            channel=Announcement.Channel.SMS,
            created_by=user,
        )

        self.assertEqual(str(announcement), "Réunion de prière")
        self.assertEqual(announcement.recipient_count, 0)
