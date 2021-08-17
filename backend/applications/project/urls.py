from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'question', views.QuestionViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'mcq_answer', views.MCQAnswerViewSet)
router.register(r'user_answer', views.UserAnswerViewSet)

urlpatterns = [
    path('', include(router.urls))
]
