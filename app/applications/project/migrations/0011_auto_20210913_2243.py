# Generated by Django 3.2.7 on 2021-09-13 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20210913_2240'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projecttype',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='questiontype',
            unique_together={('name',)},
        ),
    ]