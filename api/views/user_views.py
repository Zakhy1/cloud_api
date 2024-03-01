from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets

from api.serializers.user_serializers import UserSerializerCreate, AuthTokenSerializer
from cloud_api.generics.common import response_error, response_success


class UserViewSet(viewsets.ViewSet):
    @action(methods=('post',), url_path='register', detail=False, permission_classes=())
    def register(self, request):
        serializer = UserSerializerCreate(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({
                'success': True,
                'message': 'Success',
                'token': token.key
            })
        return response_error(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(methods=('get',), url_path='logout', detail=False)
    def logout(self, request):
        user = self.request.user
        Token.objects.get(user=user).delete()
        return response_success('Logout')

    @action(methods=('post',), url_path='login', detail=False, permission_classes=())
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'success': True,
                             'message': 'Success',
                             'token': token.key})
        return response_error(serializer.errors, status.HTTP_403_FORBIDDEN)
