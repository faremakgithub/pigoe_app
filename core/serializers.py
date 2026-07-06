from rest_framework import serializers

from .models import Church, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "country", "timezone", "created_at"]
        read_only_fields = ["created_at"]


class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = [
            "id", "organization", "legacy_id", "hierarchy", "name",
            "address", "location", "annex_count", "domain",
            "member_count", "founded_at", "photo_main", "photo_secondary",
            "created_by", "created_at", "updated_at", "deleted_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
