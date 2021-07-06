# Generated by Django 3.2.5 on 2021-07-06 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0002_alter_address_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['id_address']},
        ),
        migrations.AlterField(
            model_name='address',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL),
        ),
    ]
