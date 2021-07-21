from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the owner of the object and the user in the request are the same user.
        """
        permission_1, permission_2, permission_3 = None, None, None
        if hasattr(obj, 'owner'):
            permission_1 = obj.owner == request.user
        if hasattr(obj, 'id'):
            permission_2 = obj.id == request.user.id
        permission_3 = request.user.is_staff
        return permission_1 or permission_2 or permission_3
