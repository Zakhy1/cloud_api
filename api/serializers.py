from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from api.models import File, Access
from django.utils.translation import gettext_lazy as _


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


class UserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    @staticmethod
    def validate_password(password):
        """
        Validate password
        """
        validate_password(password)
        return password


class UserAccessSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('fullname', 'email', 'type')

    def get_fullname(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def get_type(self, obj):
        return 'co_author' if hasattr(obj, 'co_author') else 'author'


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
