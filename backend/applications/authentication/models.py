from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# class User(AbstractUser):
#     """
#     Custom model class of User.
#     """
#     username = models.CharField(max_length=20, unique=True)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     # is_active = models.BooleanField(default=False)

#     REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
#     objects = UserManager()

#     def __str__(self):
#         return self.email


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Address(models.Model):
    """
    Model defined to host the address of the users.
    """
    id_address = models.AutoField(primary_key=True)
    num = models.CharField(max_length=5)
    street = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='address', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id_address']
        db_table = 'authentication_address'
        unique_together = ['owner_id']
