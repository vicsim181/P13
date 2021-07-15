from datetime import time, timedelta
from rest_framework import serializers
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    publication = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    creator = serializers.ReadOnlyField(source='creator.email')

    def publicate(self, instance):
        
        instance['end_date'] = instance['publication'] + timedelta(days=90)
        return instance

    class Meta:
        model = models.Project
        fields = '__all__'
