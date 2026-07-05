from rest_framework import serializers

from .models import Contribution


class ContributionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contribution
        fields = [
            "id", "organization", "member", "type", "amount", "payment_method",
            "status", "paydunya_token", "receipt_number", "cancellation_reason",
            "created_by", "created_at",
        ]
        # paydunya_token : géré par le callback ADR-0014, jamais par le client API
        read_only_fields = ["paydunya_token", "created_at"]
