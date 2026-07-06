from django.contrib import admin

from .models import Church, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "timezone", "created_at"]


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = [
        "name", "hierarchy", "location", "annex_count", "member_count",
        "created_at",
    ]
    list_filter = ["hierarchy"]
    search_fields = ["name", "address", "location"]
