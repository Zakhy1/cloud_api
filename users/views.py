from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializerCreate, AuthTokenSerializer


class RegisterView(APIView):
    permission_classes = ()

    def post(self, request):
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class DeleteAuthToken(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        Token.objects.get(user=user).delete()
        return Response({
            'success': True,
            'message': 'logout'
        })
