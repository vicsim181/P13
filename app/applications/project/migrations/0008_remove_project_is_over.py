# Generated by Django 3.2.5 on 2021-08-26 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_alter_project_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='is_over',
        ),
    ]
