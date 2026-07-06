from rest_framework import serializers

from .models import Attendance, Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "organization", "church", "event_type", "legacy_id",
            "title", "description", "location", "start_at",
            "is_recurring", "reminder_hours_before", "reminder_sent_at",
            "created_at", "updated_at",
        ]
        read_only_fields = ["reminder_sent_at", "created_at", "updated_at"]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id", "event", "member", "present", "role", "note",
            "checked_in_at", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
