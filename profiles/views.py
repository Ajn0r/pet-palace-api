from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    Class to display all profiles
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Class to edit profiles
    """
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer