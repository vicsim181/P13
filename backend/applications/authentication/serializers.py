from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Address
        fields = ['id_address', 'owner', 'num', 'street', 'postal_code', 'city']


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer used to create a new user.
    """
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(message='This email already exists',
                                                                              queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True, min_length=8, max_length=89,
                                     style={'input_type': 'password'}, validators=[validate_password])
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'date_joined']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the User instance.
    Hashes the password of the new user when created through API POST request.
    """
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(message='This email already exists',
                                                                              queryset=User.objects.all())])
    address = serializers.HyperlinkedRelatedField(view_name='address-detail', read_only=True, many=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'address']
