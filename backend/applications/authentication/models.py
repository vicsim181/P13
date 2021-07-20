import uuid
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUser(AbstractUser):
    """
    Custom model class of User.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Si 'id_user', pose problème pour obtenir token avec Simple JWT
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


class Address(models.Model):
    """
    Model defined to host the address of the users.
    """
    id_address = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num = models.CharField(max_length=5)
    street = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, related_name='address', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id_address']
        db_table = 'authentication_address'
        unique_together = ['owner']
