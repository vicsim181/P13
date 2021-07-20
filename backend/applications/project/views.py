import datetime
from django.db.models.query import InstanceCheckMeta
from django.shortcuts import render
from django.http import Http404
from django.db import IntegrityError
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
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
        type = serializer.validated_data['project_type']
        type = models.Project.define_project_type(user.id, type)
        serializer.save(owner=user, project_type=type)
        return

    def list(self, request):
        context = {'request': request}
        queryset = models.Project.objects.filter(ready_for_publication=True)
        if not queryset:
            raise Http404("No MyModel matches the given query.")
        serializer = serializers.ProjectSerializer(queryset, context=context, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list' or self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # project = models.Project.objects.get(name=serializer.project)
        # project_owner = models.CustomUser.objects.get(id=project.owner.id)
        # serializer.save(owner=project_owner)
        serializer.save(owner=self.request.user)
        return


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

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
        serializer.save(owner=user, publication=datetime.datetime.now())
        return


class LikeViews(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = models.Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):
        user = self.request.user
        response = models.Project.like_project(project_id, user.id)
        return Response(response)

    def delete(self, request, project_id):
        user = self.request.user
        pass


class ProjectPublication(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get(self, project_id):
        questions_for_the_project = models.Question.objects.filter(project=project_id)
        print(questions_for_the_project)
        if questions_for_the_project:
            return Response(True)
        else:
            return Response(False)
