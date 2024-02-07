import uuid

from django.db import models

from cloud_api import settings


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files')
    file_id = models.UUIDField(unique=True, default=uuid.uuid4())
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Access(models.Model):
    file = models.ForeignKey('File', related_name='accesses', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accesses', on_delete=models.CASCADE)
