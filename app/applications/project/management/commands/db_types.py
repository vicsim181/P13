import json
from django.core.management.base import BaseCommand, CommandError
from applications.project.models import ProjectType, QuestionType


class Command(BaseCommand):
    help = 'Feed the database with the Project and Question types.'

    def handle(self, *args, **options):
        try:
            with open('applications/project/management/commands/types.json', 'r', encoding='utf-8') as types:
                data = json.load(types)
            project_types = data['project_types']
            question_types = data['question_types']
            for element in project_types:
                type = ProjectType(name=element)
                type.save()
            for element in question_types:
                type = QuestionType(name=element)
                type.save()
        except type.DoesNotExist:
            raise CommandError('No types in the types.json.')
