from django.db.models import Count
from rest_framework import generics, filters
from .models import Profile
from .serializers import ProfileSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    Class to display all profiles
    inspired by the Code Institute
    django rest walkthrough project
    """
    queryset = Profile.objects.annotate(
        nr_of_post=Count('owner__post', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'nr_of_post'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Class to edit profiles
    inspired by the Code Institute
    django rest walkthrough project
    """
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
