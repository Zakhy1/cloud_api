import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from cloud_api import settings
from cloud_api.generics.managers import UserManager


class File(models.Model):
    file_id = models.UUIDField(unique=True, default=uuid.uuid4(), primary_key=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Access(models.Model):
    file = models.ForeignKey('File', related_name='accesses', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accesses', on_delete=models.CASCADE)
    author = models.BooleanField(default=False)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
