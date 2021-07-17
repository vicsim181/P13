import datetime
from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from . import models, serializers
from ..permissions import IsOwnerOrAdmin


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'list' or self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=self.request.user)
        if not user.is_staff:
            serializer.save(project_type=models.ProjectType.objects.get(name='Pétition'))
        return

    def list(self, request):
        context = {'request': request}
        queryset = models.Project.objects.filter(ready_for_publication=True)
        if not queryset:
            raise Http404("No MyModel matches the given query.")
        serializer = serializers.ProjectSerializer(queryset, context=context, many=True)
        return Response(serializer.data)

    def publicate(self, serializer):
        serializer.save(publication=datetime.datetime.now())
        serializer.save(end_date=serializer.publication + datetime.timedelta(days=90))
        return


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer


# class ProjectTypeViewSet(viewsets.ModelViewSet):
#     queryset = models.ProjectType.objects.all()
#     serializer_class = serializers.ProjectTypeSerializer
