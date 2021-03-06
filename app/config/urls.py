"""participons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from applications import authentication, project
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from applications.project.urls import router as projectrouter
from applications.authentication.urls import router as authenticationrouter


router = DefaultRouter()
router.registry.extend(projectrouter.registry)
router.registry.extend(authenticationrouter.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token_obtain', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('login', authentication.views.login, name="login"),
    path('me', authentication.views.UserDataView.as_view(), name='current_user'),
    path('like', project.views.LikeViews.as_view(), name='like-view'),
    path('publication', project.views.ProjectPublication.as_view(), name='publish-view'),
    path('project_type', project.views.ProjectTypeRetrieveView.as_view(), name='retrieve_project_type'),
    path('question_type', project.views.QuestionTypeRetrieveView.as_view(), name='retrieve_question_type'),
    path('not_published', project.views.NonPublishedProjectsView.as_view(), name='not_published'),
    path('not_published_questions', project.views.NonPublishedQuestionsView.as_view(), name='not_published_questions'),
]
