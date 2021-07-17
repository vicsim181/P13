import datetime
from rest_framework import serializers
from . import models


# class ProjectTypeSerializer(serializers.Serializer):
#     class Meta:
#         model = models.ProjectType
#         fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    publication = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    is_over = serializers.ReadOnlyField()
    # ready_for_publication = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.email')
    question = serializers.HyperlinkedRelatedField(view_name='question-detail', read_only=True, many=True)

    # def publicate(self, instance):
    #     instance['publication'] = datetime.datetime.now()
    #     instance['end_date'] = instance['publication'] + datetime.timedelta(days=90)
    #     return instance

    class Meta:
        model = models.Project
        fields = '__all__'
        # exclude = ['ready_for_publication']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = '__all__'
