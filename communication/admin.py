from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        "title", "channel", "target_family", "recipient_count",
        "sent_at", "scheduled_at",
    ]
    list_filter = ["channel", "organization"]
    readonly_fields = ["sent_at", "recipient_count"]
