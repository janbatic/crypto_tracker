from django.contrib.auth.models import AbstractUser
from django.db import models


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
