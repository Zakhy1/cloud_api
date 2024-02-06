import uuid

from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import File


class FileSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField()
    )


class FileToUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',)


class UploadedFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('name', 'url', 'file_id')
        read_only_fields = ('name', 'url', 'file_id')

    def get_url(self, obj):
        return f'http:/127.0.0.1:8000/files/{obj.file_id}'
