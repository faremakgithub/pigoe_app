from django.contrib import admin

from .models import Contribution


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    # US-10/US-11 : historique et récapitulatif des cotisations
    list_display = [
        "member", "type", "amount", "payment_method", "status", "created_at",
    ]
    list_filter = ["type", "payment_method", "status", "organization"]
    search_fields = ["member__first_name", "member__last_name", "receipt_number"]
    readonly_fields = ["paydunya_token", "created_at"]
    date_hierarchy = "created_at"
