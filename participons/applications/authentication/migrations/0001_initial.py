# Generated by Django 3.2.5 on 2021-07-08 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id_address', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.CharField(max_length=5)),
                ('street', models.CharField(max_length=50)),
                ('postal_code', models.IntegerField()),
                ('city', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'authentication_address',
                'ordering': ['id_address'],
            },
        ),
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(fields=('owner_id',), name='unique_address_owner'),
        ),
    ]
