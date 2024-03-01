from rest_framework import status
from rest_framework.response import Response


def response_error(message, response_status=status.HTTP_400_BAD_REQUEST):
    return Response({'success': False, 'message': message}, status=response_status)


def response_success(message, response_status=status.HTTP_200_OK):
    return Response({'success': True, 'message': message}, status=response_status)
