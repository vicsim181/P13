from applications.project import models
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


class IsPublishedOrNot(permissions.BasePermission):
    """
    Custom permission to only retrieve a project that is published if the user looking for it is not an admin or the owner of it.
    """
    def has_object_permission(self, request, view, obj):
        if obj.ready_for_publication:
            return True
        else:
            if obj.owner == request.user:
                return True
            elif request.user.is_staff:
                return True
            else:
                return False


class QuestionOfPublishedProject(permissions.BasePermission):
    """
    Custom permission called when requesting a list of the questions, in order to return only the questions belonging to a published project
    """
    def has_object_permission(self, request, view, obj):
        if obj.project.ready_for_publication:
            return True
        elif obj.owner == request.user:
            return True
        elif request.user.is_staff:
            return True
        else:
            return False


class IsPublishedPetition(permissions.BasePermission):
    """
    Custom permission called when requesting to comment or like a petition
    """
    def has_object_permission(self, request, view, obj):
        petition_type = models.ProjectType.objects.get(name='Pétition')
        if not request.user.is_authenticated:
            return False
        if not obj.project_type == petition_type:
            return False
        else:
            if not obj.ready_for_publication:
                return False
            else:
                return True


class MCQAnswerOfPublishedProject(permissions.BasePermission):
    """
    Custom permission called when requesting to list or retrieve a mcqanswer
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        question = obj.question
        project = question.project
        if project.ready_for_publication:
            return True
        if question.owner == request.user:
            return True
        if request.user.is_staff:
            return True
        else:
            return False


class MCQAnswerCreatorOwnerOfQuestion(permissions.BasePermission):
    """
    Custom permission called when requesting to create, update or delete a mcqanswer
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user == obj.owner:
            return True
        if request.user.is_staff:
            return True
        else:
            return False


class OnwerOfMCQAnswer(permissions.BasePermission):
    """
    Custom permission called when requestion to update or delete a mcqanswer
    """
    def has_object_permission(self, request, view, obj):
        question = obj.question
        if not request.user.is_authenticated:
            return False
        if request.user == question.owner:
            return True
        if request.user.is_staff:
            return True
        else:
            return False
