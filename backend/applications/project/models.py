from datetime import timedelta
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from ..authentication.models import CustomUser


# Create your models here.
class ProjectType(models.Model):
    id_project_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    id_project = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    place = models.CharField(max_length=100)
    publication = models.DateTimeField(null=True)
    description = models.TextField()
    project_type = models.ForeignKey(ProjectType, related_name='project', on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='project', on_delete=models.CASCADE)
    is_over = models.BooleanField(default=False)
    end_date = models.DateTimeField(null=True)
    ready_for_publication = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


# class Form(models.Model):
#     id_form = models.AutoField(primary_key=True)
#     project = models.ForeignKey(Project, related_name='form', on_delete=models.CASCADE)


class Question(models.Model):
    id_question = models.AutoField(primary_key=True)
    wording = models.CharField(max_length=200)
    question_type = models.ForeignKey('QuestionType', related_name='question', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='form', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.wording


class QuestionType(models.Model):
    id_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class MultipleChoiceAnswer(models.Model):
    id_answer = models.AutoField(primary_key=True)
    wording = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name='multiplechoiceanswer', on_delete=models.CASCADE)


class UserAnswer(models.Model):
    user = models.ForeignKey(CustomUser, related_name='useranswer', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='useranswer', on_delete=models.CASCADE)
    answer = models.TextField()


class UserProject(models.Model):
    project = models.ForeignKey(Project, related_name='userproject', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='userproject', on_delete=models.CASCADE)
    has_participated = models.BooleanField(default=False)
