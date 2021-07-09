from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'address', views.AddressViewSet)
# router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/register/', views.UserRegisterView.as_view(), name='registration'),
    path('users/me/', views.UserDataView.as_view(), name='user-detail'),
    path('users/', views.UserListView.as_view(), name='users-list'),
]
