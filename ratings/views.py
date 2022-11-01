from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Rating
from .serializers import RatingSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'petsitting__petsitter',
        'owner',
        'rate'
    ]
    ordering_fields = [
        'rate',
        'created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadOnly]
