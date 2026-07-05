from rest_framework import viewsets

from .models import Family, Member
from .serializers import FamilySerializer, MemberSerializer


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related("family").all()
    serializer_class = MemberSerializer
