from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'address', views.AddressViewSet)

urlpatterns = [
path('', include(router.urls)),
]