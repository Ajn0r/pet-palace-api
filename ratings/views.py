from rest_framework import generics, permissions
from .models import Rating
from .serializers import RatingSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
