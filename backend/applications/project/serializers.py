import datetime
from rest_framework import serializers
from . import models
from ..authentication.serializers import CustomUser


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    publication = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    is_over = serializers.ReadOnlyField()
    ready_for_publication = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.id')
    question = serializers.HyperlinkedRelatedField(view_name='question-detail', read_only=True, many=True)
    comment = serializers.HyperlinkedRelatedField(view_name='comment-detail', read_only=True, many=True)
    liked_by = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = models.Project
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = models.Question
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    publication = serializers.DateTimeField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = models.Comment
        fields = '__all__'


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectType
        fields = '__all__'


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionType
        fields = '__all__'


class MCQAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MCQAnswer
        fields = '__all__'
