# from django.shortcuts import render
# from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework import permissions
from .permissions import IsOwnerOrAdmin
from .models import Address, CustomUser
from .serializers import AddressSerializer, UserRegisterSerializer, UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """
    Class allowing to 
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserRegisterView(generics.CreateAPIView):
    """
    Class allowing a new user to register.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserDataView(generics.RetrieveDestroyAPIView):
    """
    Class allowing a user to consult its data.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """
    Class allowing the Admin to consult the list of users registered.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
