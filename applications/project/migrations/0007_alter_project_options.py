# Generated by Django 3.2.5 on 2021-08-24 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20210818_2048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['publication']},
        ),
    ]