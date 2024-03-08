from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.models import User
from cloud_api.generics.exceptions import LoginFailed


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

    @staticmethod
    def get_fullname(obj):
        return f'{obj.first_name} {obj.last_name}'

    @staticmethod
    def get_type(obj):
        return 'co_author' if hasattr(obj, 'co_author') else 'author'


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_('Email'),
        write_only=True
    )
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise LoginFailed()
            attrs['user'] = user

        return attrs
