from rest_framework import serializers

from .models import Attendance, Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "organization", "title", "description", "location",
            "start_at", "is_recurring", "reminder_hours_before",
            "reminder_sent_at", "created_at",
        ]
        read_only_fields = ["reminder_sent_at", "created_at"]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "event", "member", "present", "checked_in_at"]
