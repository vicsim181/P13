from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers
from .models import Address


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff', 'password']


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Address
        fields = ['id', 'num', 'street', 'postal_code', 'city', 'user']
