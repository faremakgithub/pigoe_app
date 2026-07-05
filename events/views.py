from rest_framework import viewsets

from .models import Attendance, Event
from .serializers import AttendanceSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("event", "member").all()
    serializer_class = AttendanceSerializer
