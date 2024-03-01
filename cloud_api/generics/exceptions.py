from rest_framework import status
from rest_framework.exceptions import APIException


class LoginFailed(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Login failed'
