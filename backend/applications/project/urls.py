from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'question', views.QuestionViewSet)
# router.register(r'project_type', views.ProjectTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
