from django.contrib import admin

from .models import Attendance, Event


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    autocomplete_fields = ["member"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start_at", "location", "is_recurring", "organization"]
    list_filter = ["organization", "is_recurring"]
    date_hierarchy = "start_at"
    inlines = [AttendanceInline]
