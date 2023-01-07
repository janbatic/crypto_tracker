from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.dispatch import receiver

from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token as AuthToken
import logging


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.email

    def create_user(self, username, email, password, password_again):
        try:
            self.username = username
            self.email = email
            self.password = password
            self.save()
            return self
        except Exception as e:
            return e


@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, **kwargs):
    # Create user's authentication token, he will use it to auth and make all requests.
    if created:
        try:
            AuthToken.objects.get_or_create(user=instance)
        except Exception as e:
            logger = logging.getLogger('cmd')
            logger.error(f"Failed creating AuthToken for user {instance} -> {e}")
