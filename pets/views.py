from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from pet_palace_api.permissions import IsOwnerOrReadOnly
from .models import Pet
from .serializers import PetSerializer


class PetList(generics.ListCreateAPIView):
    """
    Class for viewing pets and creating
    if user is logged in
    """
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Pet.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter]

    filterset_fields = [
        'type',
        'owner',
        'owner__followed__owner__profile'
    ]

    search_fields = [
        'name',
        'owner__username',
        'description'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Class for viewing, updating and deleting
    pets.
    """
    serializer_class = PetSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Pet.objects.all().order_by('-created_at')
