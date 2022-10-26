from rest_framework import generics, permissions
from .models import PetSitting
from .serializers import PetSittingSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly
from pet_palace_api.filters import IsMsgOwnerFilterBackend


class PetSittingList(generics.ListCreateAPIView):
    queryset = PetSitting.objects.all()
    serializer_class = PetSittingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
