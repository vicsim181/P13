from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Address, CustomUser


class AddressSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

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
                                                                              queryset=CustomUser.objects.all())])
    password = serializers.CharField(required=True, write_only=True, min_length=8, max_length=89,
                                     style={'input_type': 'password'}, validators=[validate_password])
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'date_joined']

    def create(self, validated_data):
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username="Anonyme",
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the User instance. Used when a user consults his account.
    """
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(message='This email already exists',
                                                                              queryset=CustomUser.objects.all())])
    # password = serializers.CharField(required=True, min_length=8, write_only=True, style={'input_type': 'password'}, validators=[validate_password])
    address = serializers.HyperlinkedRelatedField(view_name='address-detail', read_only=True, many=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'address']
