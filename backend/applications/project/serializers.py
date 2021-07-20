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
    # ready_for_publication = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.email')
    question = serializers.HyperlinkedRelatedField(view_name='question-detail', read_only=True, many=True)
    comment = serializers.HyperlinkedRelatedField(view_name='comment-detail', read_only=True, many=True)
    liked_by = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = models.Project
        fields = '__all__'
        # exclude = ['ready_for_publication']


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = models.Question
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    publication = serializers.DateTimeField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = models.Comment
        fields = '__all__'
