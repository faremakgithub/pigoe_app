from django.contrib import admin

from .models import AccountPlan, Contribution, LedgerEntry


@admin.register(AccountPlan)
class AccountPlanAdmin(admin.ModelAdmin):
    list_display = ["account_number", "title", "organization", "church", "account_type"]
    list_filter = ["account_type", "organization"]
    search_fields = ["title", "account_number", "description"]


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ["title", "organization", "church", "account_plan", "debit", "credit", "operation_date"]
    list_filter = ["organization", "church", "account_plan"]
    search_fields = ["title", "description", "reference_number"]
    date_hierarchy = "operation_date"


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
