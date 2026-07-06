from django.contrib import admin

from .models import Attendance, Event, EventType


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "organization", "created_at", "updated_at"]
    search_fields = ["name", "description"]


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    autocomplete_fields = ["member"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start_at", "location", "is_recurring", "organization", "event_type"]
    list_filter = ["organization", "is_recurring", "event_type"]
    date_hierarchy = "start_at"
    inlines = [AttendanceInline]
