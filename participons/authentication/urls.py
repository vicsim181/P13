from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'address', views.AddressViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
path('', include(router.urls)),
]
