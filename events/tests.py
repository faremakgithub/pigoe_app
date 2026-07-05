from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from core.models import Organization
from members.models import Member

from .models import Attendance, Event


class EventModelTests(TestCase):
    def test_str_returns_title(self):
        org = Organization.objects.create(name="Église Test")
        event = Event.objects.create(
            organization=org,
            title="Culte du dimanche",
            location="Bassar",
            start_at=timezone.now(),
        )

        self.assertEqual(str(event), "Culte du dimanche")
        self.assertEqual(event.reminder_hours_before, 24)


class AttendanceModelTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Église Test")
        self.event = Event.objects.create(
            organization=self.org,
            title="Culte du dimanche",
            location="Bassar",
            start_at=timezone.now(),
        )
        self.member = Member.objects.create(
            organization=self.org,
            first_name="Kodjo",
            last_name="Mensah",
            phone="+22890123456",
        )

    def test_create_attendance(self):
        attendance = Attendance.objects.create(event=self.event, member=self.member, present=True)

        self.assertIn("présent", str(attendance))

    def test_duplicate_attendance_for_same_member_and_event_is_rejected(self):
        # US-15/US-16 : un seul pointage par membre et par événement
        Attendance.objects.create(event=self.event, member=self.member)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Attendance.objects.create(event=self.event, member=self.member)
