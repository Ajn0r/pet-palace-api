from django.db.models import Q
from rest_framework import filters


class IsMsgOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Custom filter for the AppMessage views
    only displaying the messages that is
    connected to either the sender or
    the reciver.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            Q(owner=request.user.id) | Q(reciver=request.user.id))
