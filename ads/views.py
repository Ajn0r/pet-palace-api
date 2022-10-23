from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ad
from .serializers import AdSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class AdList(generics.ListAPIView):
    queryset = Ad.objects.filter(status=1)
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'type',
        'pets']


class AdCreate(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
