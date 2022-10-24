from django.db.models import Q
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from pet_palace_api.permissions import IsOwnerOrReadOnly
from .models import AppMessage
from .serializers import AppMessageSerializer


class AppMessageList(generics.ListAPIView):
    serializer_class = AppMessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
        ]
    filterset_fields = [
        'owner',
    ]
    search_fields = [
        'subject'
    ]

    def get_queryset(self):
        return AppMessage.objects.all().filter(
            Q(owner=self.request.user.id) | Q(reciver=self.request.user.id))


class AppMessageCreate(generics.CreateAPIView):

    serializer_class = AppMessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = AppMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
