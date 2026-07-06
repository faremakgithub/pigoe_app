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
            "id", "organization", "church", "legacy_id", "family",
            "membership_number", "has_left", "is_deceased", "first_name",
            "last_name", "full_name", "phone", "email", "sex",
            "birth_date", "birth_place", "address", "profession",
            "nationality", "baptism_date", "baptism_place", "member_group",
            "conversion_date", "conversion_place", "holy_spirit_date",
            "holy_spirit_place", "marital_status", "children_count",
            "spouse", "guardian", "parent_contact", "activities",
            "member_type", "status", "deleted_at", "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
