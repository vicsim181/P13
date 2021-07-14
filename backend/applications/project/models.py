from django.db import models
from django.db.models.deletion import CASCADE
from ..authentication.models import CustomUser


# Create your models here.
class Project(models.Model):
    id_project = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    place = models.CharField(max_length=100)
    publication = models.DateTimeField()
    description = models.TextField()
    id_project_type = models.ForeignKey('ProjectType', related_name='project', on_delete=models.CASCADE)
    creator_email = models.EmailField()
    is_over = models.BooleanField(default=False)
    end_date = models.DateTimeField()  # METTRE DATE DE FIN PAR DEFAUT A 3 MOIS DE PLUS QUE PUBLICATION


class Form(models.Model):
    id_form = models.AutoField(primary_key=True)
    id_project = models.ForeignKey(Project, related_name='form', on_delete=models.CASCADE)


class ProjectType(models.Model):
    id_project_type = models.AutoField(primary_key=True)
    name = models.CharField()


class Question(models.Model):
    id_question = models.AutoField(primary_key=True)
    wording = models.CharField(max_length=200)
    id_question_type = models.ForeignKey('QuestionType', related_name='question', on_delete=models.CASCADE)
    id_form = models.ForeignKey(Form, related_name='question', on_delete=models.CASCADE)


class MultipleChoiceAnswer(models.Model):
    id_answer = models.AutoField(primary_key=True)
    wording = models.CharField()
    id_question = models.ForeignKey(Question, related_name='multiple-choice-answer', on_delete=CASCADE)


class UserAnswer(models.Model):
    id_user = models.ForeignKey(CustomUser, related_name='user-answer', on_delete=CASCADE)
    id_question = models.ForeignKey(Question, related_name='user-answer', on_delete=CASCADE)
    answer = models.CharField()


class UserProject(models.Model):
    id_project = models.ForeignKey(Project, related_name='user-project', on_delete=CASCADE)
    id_user = models.ForeignKey(CustomUser, related_name='user-project', on_delete=CASCADE)
    has_participated = models.BooleanField(default=False)
