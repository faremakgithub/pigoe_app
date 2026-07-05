from rest_framework import serializers

from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            "id", "organization", "title", "message", "channel",
            "target_family", "scheduled_at", "sent_at", "recipient_count",
            "created_by", "created_at",
        ]
        read_only_fields = ["sent_at", "recipient_count", "created_at"]
