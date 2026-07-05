from django.contrib import admin

from .models import Family, Member


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ["name", "organization", "created_at"]
    list_filter = ["organization"]
    search_fields = ["name"]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # US-04 : recherche et filtrage des membres
    list_display = ["full_name", "phone", "family", "status", "created_at"]
    list_filter = ["status", "family", "organization"]
    search_fields = ["first_name", "last_name", "phone"]
    autocomplete_fields = ["family"]
