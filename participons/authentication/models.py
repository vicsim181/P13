from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
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
