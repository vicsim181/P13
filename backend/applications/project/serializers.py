import datetime
import datetime
from rest_framework import serializers
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    publication = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    is_over = serializers.ReadOnlyField()
    ready_for_publication = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.email')
    question = serializers.ReadOnlyField(source='question.wording')

    def publicate(self, instance):
        instance['publication'] = datetime.datetime.now()
        instance['end_date'] = instance['publication'] + datetime.timedelta(days=90)
        return instance

    class Meta:
        model = models.Project
        fields = '__all__'
        # exclude = ['ready_for_publication']


class QuestionCreationSerializer(serializers.ModelSerializer):
    # project = serializers.Field(source='project.name')

    class Meta:
        model = models.Question
        fields = '__all__'
