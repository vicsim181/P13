import requests
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from ..permissions import IsOwnerOrAdmin
from .models import Address, CustomUser
from .serializers import AddressSerializer, UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'update':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class UserDataView(generics.RetrieveAPIView):
    """
    Class allowing a user to consult its data.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_profile = self.request.user
        serializer = UserSerializer(user_profile, context={'request': request})
        return Response({'user': serializer.data})


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = get_user_model().objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('Utilisateur non existant')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Mot de passe incorrect')

    response = Response()
    token_endpoint = reverse(viewname='token_obtain_pair', request=request)
    tokens = requests.post(token_endpoint, data=request.data).json()

    response.data = {
        'access_token': tokens.get('access'),
        'refresh_token': tokens.get('refresh'),
        'email': user.email
    }
    return response
