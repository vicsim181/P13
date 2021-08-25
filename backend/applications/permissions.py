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
        print('REQUEST USER ', request.user)
        if hasattr(obj, 'owner'):
            permission_1 = obj.owner == request.user
        if hasattr(obj, 'id'):
            permission_2 = obj.id == request.user.id
        permission_3 = request.user.is_staff
        print('permission 1 ', permission_1, ' permission 2 ', permission_2, ' permission 3 ', permission_3)
        return permission_1 or permission_2 or permission_3


class IsPublishedOrNot(permissions.BasePermission):
    """
    Custom permission to only retrieve a project that is published if the user looking for it is not an admin or the owner of it.
    """
    def has_object_permission(self, request, view, obj):
        print('REQUEST USER ', request.user)
        print('OBJ  ', obj.ready_for_publication)
        if obj.ready_for_publication:
            return True
        else:
            if obj.owner == request.user:
                print('obj owner and request user TRUE')
                return True
            elif request.user.is_staff:
                print('obj owner and request user FALSE and user is staff')
                return True
            else:
                print('obj owner and request user FALSE and user is NOT staff')
                return False
