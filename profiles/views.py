from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
