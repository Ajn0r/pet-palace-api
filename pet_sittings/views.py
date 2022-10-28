from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import PetSitting
from .serializers import PetSittingSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class PetSittingList(generics.ListCreateAPIView):
    queryset = PetSitting.objects.annotate(
        nr_of_pets_to_sit=Count('pets')
    )
    serializer_class = PetSittingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner',
        'pets',
        'petsitter',
        'status',
        'owner__profile'
    ]
    ordering_fields = [
        'date_from',
        'date_to',
        'created_at',
        'status'
    ]
    search_fields = [
        'pets__name',
        'location',
        'description'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetSittingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSittingSerializer
    queryset = PetSitting.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
