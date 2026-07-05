from rest_framework import serializers

from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "country", "timezone", "created_at"]
        read_only_fields = ["created_at"]
