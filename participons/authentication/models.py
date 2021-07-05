from django.db import models
from django.db.models.base import Model
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE


class Address(models.Model):
    """
    Model defined to host the address of the users.
    """
    num = models.CharField(max_length=5)
    street = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), related_name='address', on_delete=CASCADE)
