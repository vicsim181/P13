from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Address
        fields = ['id_address', 'owner', 'num', 'street', 'postal_code', 'city']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the User instance.
    Hashes the password of the new user when created through API POST request.
    """
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, max_length=89, style={'input_type': 'password'})
    address = serializers.HyperlinkedRelatedField(view_name='address-detail', read_only=True, many=True)
    date_joined = serializers.DateTimeField()

    # def create(self, validated_data):
    #     user = super(UserSerializer, self).create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'date_joined', 'address']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
