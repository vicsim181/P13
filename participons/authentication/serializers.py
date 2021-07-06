from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Address
        fields = ['id_address', 'owner', 'num', 'street', 'postal_code', 'city']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User instance.
    Hashes the password of the new user when created through API POST request.
    """
    address = serializers.ReadOnlyField(source='address.id')
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'address', 'is_staff']