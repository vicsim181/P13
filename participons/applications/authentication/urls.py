from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'address', views.AddressList)
router.register(r'users', views.UserViewSet)

urlpatterns = [
path('', include(router.urls)),
path('address/', views.AddressList.as_view()),
path('address/<int:pk>/', views.AddressDetail.as_view()),
path('address/create/', views.AddressCreation.as_view()),
]
