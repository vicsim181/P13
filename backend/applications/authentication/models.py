import uuid
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser, UserManager
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    """
    Custom model class of User.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(default="", max_length=7)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    objects = UserManager()

    def __str__(self):
        return self.email


# @receiver(post_save, sender=CustomUser)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class Address(models.Model):
    """
    Model defined to host the address of the users.
    """
    id_address = models.AutoField(primary_key=True)
    num = models.CharField(max_length=5)
    street = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, related_name='address', on_delete=CASCADE)

    class Meta:
        ordering = ['id_address']
        db_table = 'authentication_address'
        unique_together = ['owner_id']
