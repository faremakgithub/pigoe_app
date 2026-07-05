from rest_framework import viewsets

from .models import Contribution
from .serializers import ContributionSerializer


class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.select_related("member").all()
    serializer_class = ContributionSerializer

    def perform_create(self, serializer):
        # US-12 traçabilité : l'auteur d'une transaction est toujours
        # l'utilisateur authentifié, jamais une valeur fournie par le client.
        serializer.save(created_by=self.request.user)
