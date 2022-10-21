from rest_framework import generics, permissions
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
