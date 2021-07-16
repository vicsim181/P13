from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'question', views.QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
