from django.db.models import Q
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from pet_palace_api.permissions import IsOwnerOrReadOnly
from pet_palace_api.filters import IsMsgOwnerFilterBackend
from .models import AppMessage
from app_messages import serializers


class AppMessageList(generics.ListAPIView):
    serializer_class = serializers.AppMessageSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]
    queryset = AppMessage.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        IsMsgOwnerFilterBackend
        ]
    filterset_fields = [
        'owner',
    ]
    search_fields = [
        'subject'
    ]


class AppMessageCreate(generics.CreateAPIView):
    serializer_class = serializers.CreateAppMessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = AppMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AppMessageDetail(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.AppMessageSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = AppMessage.objects.all()
    filter_backends = [IsMsgOwnerFilterBackend]
