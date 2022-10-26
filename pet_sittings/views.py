from django.db.models import Count
from rest_framework import generics, permissions
from .models import PetSitting
from .serializers import PetSittingSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly
from pet_palace_api.filters import IsMsgOwnerFilterBackend


class PetSittingList(generics.ListCreateAPIView):
    queryset = PetSitting.objects.annotate(
        nr_of_pets_to_sit=Count('pets')
    )
    serializer_class = PetSittingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetSittingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSittingSerializer
    queryset = PetSitting.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
