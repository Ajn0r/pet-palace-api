from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ad
from .serializers import AdSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class AdList(generics.ListCreateAPIView):
    queryset = Ad.objects.annotate(
        nr_of_interest=Count('interests'),
        )
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'type',
        'pets',
        'status',
        'owner']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AdDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrReadOnly]
