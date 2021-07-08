# from django.shortcuts import render
# from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrAdmin
from .models import Address, User
from .serializers import UserSerializer, AddressSerializer


# Create your views here.
# class AddressList(generics.ListAPIView):
#     """
#     This viewset automatically provides `list` and `retrieve` actions.
#     """
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer
#     permission_classes = [permissions.IsAdminUser]
#     filterset_fields = ['owner']


# class AddressDetail(generics.RetrieveAPIView):
#     """
#     """
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer
#     permission_classes = [IsOwnerOrAdmin]


# class AddressCreation(generics.CreateAPIView):
#     """
#     """
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

class AddressViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
