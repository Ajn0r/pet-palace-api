from django.db.models import Count, Avg
from django.contrib.auth.models import User
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
        nr_of_pets=Count('owner__pet_owner', distinct=True),
        rating=Avg('owner__petsitter__petsitting_rating__rate', distinct=True),
        nr_of_ratings=Count(
            'owner__petsitter__petsitting_rating', distinct=True),
        nr_of_sittings=Count('owner__petsitter', distinct=True),
        nr_of_msg_recived=Count('owner__message_reciver', distinct=True),
        nr_of_msg_sent=Count('owner__sender', distinct=True)
    ).order_by('-created_at').exclude(owner__is_staff=True)
    serializer_class = ProfileSerializer

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]

    ordering_fields = [
        'nr_of_post',
        'following_count',
        'followers_count',
        'owner__following__created_at',
        'owner__followed__created_at',
        'rating'
    ]

    filterset_fields = [
        'owner__following__followed__profile',
        'owner__pet_owner__type',
        'type',
    ]

    search_fields = [
        'owner__username'
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
        nr_of_post=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
        rating=Avg('owner__petsitter__petsitting_rating', distinct=True)
    ).order_by('-created_at')
