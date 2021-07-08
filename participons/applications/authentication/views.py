# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrAdmin
from .models import Address
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


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
