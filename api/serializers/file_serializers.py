from rest_framework import serializers
from api.models import File, Access


class FileSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField()
    )


class UploadedFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'name', 'url', 'file_id')
        read_only_fields = ('id', 'name', 'url', 'file_id')

    def get_url(self, obj):
        host = 'http://127.0.0.1:8000'
        # return f'{host}' + reverse('api:detail', args=(obj.id,))
        return f'{host}/files/{obj.file_id}'


class AccessSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Access
        fields = ('fullname', 'email', 'type')

    def get_fullname(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def get_type(self, obj):
        return 'author' if obj.file.owner == obj.user else 'co_author'

    def get_email(self, obj):
        return f'{obj.user.email}'


class FileWithAccessSerializer(UploadedFileSerializer):
    accesses = AccessSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = ('id', 'name', 'url', 'file_id', 'accesses')
        read_only_fields = ('id', 'name', 'url', 'file_id', 'accesses')
