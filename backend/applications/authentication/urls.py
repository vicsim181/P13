from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'address', views.AddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/address/', views.CreateAddressView.as_view(), name='address-creation'),
    path('register/', views.UserRegisterView.as_view(), name='registration'),
    path('me/', views.UserDataView.as_view(), name='user-detail'),
    path('all/', views.UserListView.as_view(), name='users-list'),
]
