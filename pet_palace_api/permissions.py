from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Class to only give logged in users and the owner
    of the object permission to handle it, 
    checks that the user is the owner.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
        