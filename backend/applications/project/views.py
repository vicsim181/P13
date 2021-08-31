import datetime
import django_filters.rest_framework
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
from django.db import IntegrityError
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from . import models, serializers
from ..permissions import IsOwnerOrAdmin, IsPublishedOrNot, QuestionOfPublishedProject


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
        serializer = serializers.ProjectSerializer(non_published_queryset, context=context, many=True)
        return Response(serializer.data)


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

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     # print("REQUEST ", self.request.data['project'])
    #     petition = models.Project.objects.get(pk=self.request.data['project'])
    #     if not petition.ready_for_publication:
    #         return False
    #     serializer.save(owner=user, publication=datetime.datetime.now())
    #     return

    def create(self, validated_data):
        petition_type = models.ProjectType.objects.get(name='Pétition')
        petition = models.Project.objects.get(pk=validated_data.data['project'])
        if petition.project_type.id_project_type == petition_type.id_project_type:
            if petition.ready_for_publication:
                response = models.Comment.objects.create(owner=self.request.user,
                                                         publication=datetime.datetime.now(),
                                                         text=validated_data.data['text'],
                                                         project=petition)
                return Response(response)
            else:
                response = HttpResponseForbidden
                return Response(response)


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
        print('REQUETE  : ', request)
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
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
