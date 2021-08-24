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
    description = models.TextField(max_length=1000)
    project_type = models.ForeignKey(ProjectType, related_name='project', on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='project', on_delete=models.CASCADE)
    is_over = models.BooleanField(default=False)
    end_date = models.DateTimeField(null=True)
    ready_for_publication = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(CustomUser, related_name='project_liked')

    class Meta:
        ordering = ['publication']

    def __str__(self) -> str:
        return self.name

    def define_project_type(user_id, type):
        creator = CustomUser.objects.get(id=user_id)
        if creator.is_staff:
            project_type = ProjectType.objects.get(name=type)
        else:
            project_type = ProjectType.objects.get(name='Pétition')
        return project_type

    def publicate_project(project, project_type_id):
        consultation_type = get_object_or_404(ProjectType, name='Consultation')
        petition_type = get_object_or_404(ProjectType, name='Pétition')
        if consultation_type == project_type_id:
            questions = get_list_or_404(Question, project=project.id_project)
        project.publication = str(datetime.datetime.now())
        if project_type_id == petition_type:
            project.end_date = str(datetime.datetime.now() + datetime.timedelta(days=90))
        project.ready_for_publication = True
        project.save()
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
    id_question_type = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class MCQAnswer(models.Model):
    id_answer = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wording = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name='mcqanswer', on_delete=models.CASCADE)


class UserAnswer(models.Model):
    id_user_answer = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, related_name='useranswer', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='useranswer', on_delete=models.CASCADE)
    answer = models.TextField(max_length=1000)

    class Meta:
        unique_together = ['user', 'question']


class Comment(models.Model):
    id_comment = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(CustomUser, related_name='comment', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    project = models.ForeignKey(Project, related_name='comment', on_delete=models.CASCADE)
    publication = models.DateTimeField()

    class Meta:
        unique_together = ['owner', 'project']
