from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from . import models, serializers
from ..permissions import IsOwnerOrAdmin


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'destroy':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
