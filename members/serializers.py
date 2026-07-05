from rest_framework import serializers

from .models import Family, Member


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["id", "organization", "name", "created_at"]
        read_only_fields = ["created_at"]


class MemberSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Member
        fields = [
            "id", "organization", "family", "first_name", "last_name",
            "full_name", "phone", "email", "status", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
