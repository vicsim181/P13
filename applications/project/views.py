import datetime

from django.db.models import query
import django_filters.rest_framework
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
from django.db import IntegrityError
from rest_framework import viewsets, permissions, generics, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from . import models, serializers
from ..permissions import IsOwnerOrAdmin, IsPublishedOrNot, IsPublishedPetition, QuestionOfPublishedProject
from ..permissions import MCQAnswerCreatorOwnerOfQuestion, MCQAnswerOfPublishedProject, OnwerOfMCQAnswer


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filterset_fields = ['owner_id', 'project_type', 'liked_by']

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsPublishedOrNot]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        type = serializer.validated_data['project_type']
        type = models.Project.define_project_type(user.id, type)
        serializer.save(owner=user, project_type=type)
        return

    def list(self, request):
        filters = {}
        for filter in request.GET:
            filters[filter] = request.GET[filter]
        context = {'request': request}
        queryset = get_list_or_404(models.Project,
                                   ready_for_publication=True,
                                   **filters)
        self.check_object_permissions(self.request, queryset)
        serializer = serializers.ProjectSerializer(queryset, context=context, many=True)
        return Response(serializer.data)


class NonPublishedProjectsView(generics.ListAPIView):
    queryset = models.Project.objects.all()
    permission_classes = [IsOwnerOrAdmin]
    filterset_fields = ['project_type']

    def get(self, request):
        context = {'request': request}
        if 'project_type' not in request.GET:
            raise APIException('Vous devez fournir un type de projet')
        if 'owner_id' not in request.GET:
            raise APIException('Vous devez fournir un owner_id')
        project_type_id = request.GET['project_type']
        owner_id = request.GET['owner_id']
        queryset = get_list_or_404(models.Project,
                                   ready_for_publication=False,
                                   owner=owner_id,
                                   project_type=project_type_id)
        for element in queryset:
            self.check_object_permissions(self.request, element)
        serializer = serializers.ProjectSerializer(queryset, context=context, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [QuestionOfPublishedProject]
        elif self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return

    def list(self, request):
        filters = {}
        for filter in request.GET:
            filters[filter] = request.GET[filter]
        context = {'request': request}
        queryset = get_list_or_404(models.Question,
                                   **filters)
        allowed_queryset = []
        for element in queryset:
            if element.project.ready_for_publication:
                allowed_queryset.append(element)
            elif request.user.is_staff:
                allowed_queryset.append(element)
        self.check_object_permissions(self.request, allowed_queryset)
        serializer = serializers.QuestionSerializer(allowed_queryset, context=context, many=True)
        return Response(serializer.data)


class NonPublishedQuestionsView(generics.ListAPIView):
    queryset = models.Question.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request):
        context = {'request': request}
        filters = {}
        for filter in request.GET:
            filters[filter] = request.GET[filter]
        context = {'request': request}
        queryset = get_list_or_404(models.Question,
                                   **filters)
        non_published_queryset = []
        for element in queryset:
            if not element.project.ready_for_publication:
                non_published_queryset.append(element)
        self.check_object_permissions(self.request, non_published_queryset)
        serializer = serializers.QuestionSerializer(non_published_queryset, context=context, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filterset_fields = ['owner', 'project']

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsPublishedPetition]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        project_id = self.request.data['project']
        project = models.Project.objects.get(pk=project_id)
        self.check_object_permissions(self.request, project)
        serializer.save(owner=user, publication=datetime.datetime.now())
        return


class LikeViews(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = models.Project.objects.all()
    permission_classes = [IsPublishedPetition]
    serializer_class = serializers.LikeSerializer

    def put(self, request):
        if 'project_id' not in request.data:
            raise APIException('Vous devez fournir un id de projet')
        if 'action' not in request.data:
            raise APIException('Vous devez fournir une action de like (add ou delete)')
        project_id = request.data['project_id']
        project = get_object_or_404(models.Project, id_project=project_id)
        action = request.data['action']
        liker_id = self.request.user.id
        self.check_object_permissions(request, project)
        response = models.Project.like_project(project_id, liker_id, action)
        serializer = serializers.LikeSerializer(response)
        return Response(serializer.data)


class ProjectPublication(APIView):
    queryset = models.Project.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def put(self, request):
        project_id = request.data['project_id']
        project = get_object_or_404(models.Project, id_project=project_id)
        self.check_object_permissions(request, project)
        project_type = project.project_type
        response = models.Project.publicate_project(project, project_type)
        serializer = serializers.ProjectSerializer(response)
        return Response(serializer.data)


class ProjectTypeRetrieveView(generics.RetrieveAPIView):
    queryset = models.ProjectType.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        type_name = request.GET['name']
        project_type = get_object_or_404(models.ProjectType, name=type_name)
        print('RESULT PROJECT TYPE ', project_type)
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
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [MCQAnswerOfPublishedProject]
        elif self.action == 'create':
            permission_classes = [MCQAnswerCreatorOwnerOfQuestion]
        elif self.action == 'destroy' or self.action == 'update':
            permission_classes = [OnwerOfMCQAnswer]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        filters = {}
        for filter in request.GET:
            filters[filter] = request.GET[filter]
        context = {'request': request}
        queryset = get_list_or_404(models.MCQAnswer,
                                   **filters)
        for element in queryset:
            self.check_object_permissions(self.request, element)
        serializer = serializers.MCQAnswerSerializer(queryset, context=context, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        question_id = self.request.data['question']
        question = models.Question.objects.get(pk=question_id)
        self.check_object_permissions(self.request, question)
        serializer.save()
        return


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = models.UserAnswer.objects.all()
    serializer_class = serializers.UserAnswerSerializer
    filterset_fields = ['question', 'owner']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        user = self.request.user
        if not user.is_authenticated:
            raise exceptions.AuthenticationFailed('Utilisateur non authentifié')
        filters = {}
        for filter in self.request.GET:
            filters[filter] = self.request.GET[filter]
        if user.is_staff:
            queryset = get_list_or_404(models.UserAnswer,
                                       **filters)
        if user.is_authenticated and not user.is_staff:
            filters['owner'] = user
            queryset = get_list_or_404(models.UserAnswer,
                                       **filters)
        context = {'request': request}
        for element in queryset:
            self.check_object_permissions(self.request, element)
        serializer = serializers.UserAnswerSerializer(queryset, context=context, many=True)
        return Response(serializer.data)
