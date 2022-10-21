from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
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
        nr_of_post=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]

    ordering_fields = [
        'nr_of_post',
        'following_count',
        'followers_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

    filterset_fields = [
        'owner__following__followed__profile'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Class to edit profiles
    inspired by the Code Institute
    django rest walkthrough project
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        post_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
