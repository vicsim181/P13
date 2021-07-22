import uuid
import datetime
from django.db import models
from django.db.utils import IntegrityError
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, get_list_or_404
from ..authentication.models import CustomUser


# Create your models here.
class ProjectType(models.Model):
    id_project_type = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    id_project = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    place = models.CharField(max_length=100)
    publication = models.DateTimeField(null=True)
    description = models.TextField()
    project_type = models.ForeignKey(ProjectType, related_name='project', on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='project', on_delete=models.CASCADE)
    is_over = models.BooleanField(default=False)
    end_date = models.DateTimeField(null=True)
    ready_for_publication = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(CustomUser, related_name='project_liked')

    def __str__(self) -> str:
        return self.name

    def define_project_type(user_id, type):
        creator = CustomUser.objects.get(id=user_id)
        if creator.is_staff:
            project_type = ProjectType.objects.get(name=type)
        else:
            project_type = ProjectType.objects.get(name='Pétition')
        return project_type

    def publicate_project(project_id):
        questions = get_list_or_404(Question, project=project_id)
        project_to_publicate = Project.objects.get(id_project=project_id)
        project_to_publicate.publication = datetime.datetime.utcnow()
        project_to_publicate.end_date = datetime.datetime.utcnow() + datetime.timedelta(days=90)
        project_to_publicate.ready_for_publication = True
        project_to_publicate.save()
        return

    def like_project(project_id, liker_id, action):
        project_to_like = get_object_or_404(Project, id_project=project_id)
        if action == 'add':
            likers = project_to_like.liked_by.all()
            for liker in likers:
                if liker_id == liker.id:
                    return
            project_to_like.liked_by.add(liker_id)
            return
        elif action == 'delete':
            likers = project_to_like.liked_by.all()
            for liker in likers:
                if liker_id == liker.id:
                    project_to_like.liked_by.remove(liker_id)
                    return
            return


class Question(models.Model):
    id_question = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wording = models.CharField(max_length=200)
    question_type = models.ForeignKey('QuestionType', related_name='question', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='question', on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='question', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.wording


class QuestionType(models.Model):
    id_type = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class MultipleChoiceAnswer(models.Model):
    id_answer = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wording = models.CharField(max_length=200)
    question = models.ManyToManyField(Question)


class UserAnswer(models.Model):
    user = models.ForeignKey(CustomUser, related_name='useranswer', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='useranswer', on_delete=models.CASCADE)
    answer = models.TextField()

    class Meta:
        unique_together = ['user', 'question']


class Comment(models.Model):
    id_comment = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(CustomUser, related_name='comment', on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    project = models.ForeignKey(Project, related_name='comment', on_delete=models.CASCADE)
    publication = models.DateTimeField()
