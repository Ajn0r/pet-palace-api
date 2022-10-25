from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from pet_palace_api.permissions import IsOwnerOrReadOnly
from .models import AdInterest
from .serializers import AdInterestSerializer


class InterestList(generics.ListCreateAPIView):
    """
    View class for ad interest
    from the Code Institute
    django rest walkthrough project
    """
    serializer_class = AdInterestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = AdInterest.objects.all()
    #filter_backends = [
    #    filters.OrderingFilter,
    #    DjangoFilterBackend]
    #filterset_fields = [
    #    'ad__pets',
    #    'ad__date_from',
    #    'ad__location',
    #    'ad__status',
    #    'ad__owner__profile__owner',
    #]
    #ordering_fields = [
    #    'ad__date_from',
    #    'ad__status'
    #]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InterestDetail(generics.RetrieveDestroyAPIView):
    """
    View class for ad interest
    from the Code Institute
    django rest walkthrough project
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AdInterestSerializer
    queryset = AdInterest.objects.all()
