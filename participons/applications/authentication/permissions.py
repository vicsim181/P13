from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the owner of the object and the user in the request are the same user.
        """
        return obj.owner == request.user or request.user.is_superuser
