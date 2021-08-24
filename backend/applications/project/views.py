import datetime
import django_filters.rest_framework
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import IntegrityError
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from ..permissions import IsOwnerOrAdmin, IsPublishedOrNot


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filterset_fields = ['id_project', 'ready_for_publication', 'owner_id', 'project_type', 'liked_by']

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'list':
            permission_classes = [IsPublishedOrNot]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsPublishedOrNot]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        type = serializer.validated_data['project_type']
        type = models.Project.define_project_type(user.id, type)
        serializer.save(owner=user, project_type=type)
        return

    def retrieve(self, request, pk):
        print('RETRIEVE REQUEST')


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list' or self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filterset_fields = ['owner', 'project']

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
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        project_id = request.data['project_id']
        action = request.data['action']
        liker_id = self.request.user.id
        self.check_object_permissions(request, liker_id)
        response = models.Project.like_project(project_id, liker_id, action)
        serializer = serializers.ProjectSerializer(response)
        return Response(serializer.data)


class ProjectPublication(APIView):
    queryset = models.Project.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def put(self, request):
        project_id = request.data['project_id']
        project = get_object_or_404(models.Project, id_project=project_id)
        self.check_object_permissions(request, project)
        project_type_id = project.project_type
        response = models.Project.publicate_project(project, project_type_id)
        serializer = serializers.ProjectSerializer(response)
        return Response(serializer.data)


class ProjectTypeRetrieveView(generics.RetrieveAPIView):
    queryset = models.ProjectType.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        type_name = request.GET['name']
        project_type = get_object_or_404(models.ProjectType, name=type_name)
        self.check_object_permissions(request, project_type)
        serializer = serializers.ProjectTypeSerializer(project_type)
        return Response(serializer.data)


class QuestionTypeRetrieveView(generics.RetrieveAPIView):
    queryset = models.QuestionType.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        type_name = request.GET['name']
        question_type = get_object_or_404(models.QuestionType, name=type_name)
        self.check_object_permissions(request, question_type)
        serializer = serializers.QuestionTypeSerializer(question_type)
        return Response(serializer.data)


class MCQAnswerViewSet(viewsets.ModelViewSet):
    queryset = models.MCQAnswer.objects.all()
    serializer_class = serializers.MCQAnswerSerializer

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list' or self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = models.UserAnswer.objects.all()
    serializer_class = serializers.UserAnswerSerializer
    filterset_fields = ['question', 'user']

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list' or self.action == 'create':
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
