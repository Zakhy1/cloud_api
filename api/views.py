import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse

from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets

from api.models import File, Access
from cloud_api.permissions import CustomIsOwner
from api.serializers import FileSerializer, UploadedFileSerializer, FileWithAccessSerializer
from users.models import User
from users.serializers import UserAccessSerializer


class FilesViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = File.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [CustomIsOwner, ]

    def list(self, request, **kwargs):
        queryset = File.objects.filter(owner=request.user)
        serializer = UploadedFileSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.initial_data['files']
            uploaded_files = []

            uploaded_file = File.objects.create(name=file.name, file_id=uuid.uuid4(),
                                                owner=request.user,
                                                file=file)
            Access.objects.create(user=request.user, file=uploaded_file)
            host = 'http://127.0.0.1:8000'
            uploaded_files.append({
                'success': True,
                'message': 'Success',
                'name': uploaded_file.name,
                'url': f'{host}/files/{uploaded_file.file_id}',
                'file_id': uploaded_file.file_id
            })
            return Response(uploaded_files, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, *args, **kwargs):
        try:
            file = File.objects.get(id=kwargs['pk'])
        except Exception:
            raise NotFound(detail=None, code=404)
        if file.owner == request.user:
            return FileResponse(open(file.file.path, 'rb'))
        raise PermissionDenied(detail='Forbidden for you', code=403)

    def update(self, request, *args, **kwargs):
        try:
            file = File.objects.get(id=kwargs['pk'])
        except Exception:
            return Response({'message': 'not found'}, status=404)
        file.name = request.data['name']
        file.save()
        if file.owner == request.user:
            return Response({
                'success': True,
                'message': 'Renamed'
            })
        raise PermissionDenied(detail='Forbidden for you', code=403)

    def destroy(self, request, *args, **kwargs):
        try:
            file = File.objects.get(id=kwargs['pk'])
        except Exception:
            return Response({'message': 'Not found'}, status=404)

        file.delete()
        return Response({
            'success': True,
            'message': 'File already deleted',
        })

    @action(methods=('post',), detail=True, url_path='accesses')
    def give_access(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['pk'])
        try:
            user = User.objects.get(email=request.data['email'])
            user.co_author = True
        except ObjectDoesNotExist:
            raise ValidationError(detail={'message': 'Enter the correct user email'}, code=422)
        if request.user != file.owner:
            raise PermissionDenied(detail='Forbidden for you', code=403)
        Access.objects.get_or_create(user=user, file=file)
        serializer = UserAccessSerializer((user, self.request.user), many=True)
        return Response(serializer.data)

    @action(methods=('get',), detail=False, url_path='shared')
    def get_shared_files(self, request, *args, **kwargs):
        user = self.request.user
        queryset = File.objects.filter(accesses__user_id=user).exclude(owner=user)
        serializer = UploadedFileSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=('get',), detail=False, url_path='disk')
    def get_all_files(self, request, *args, **kwargs):
        user = self.request.user
        files = File.objects.filter(owner=user)
        file_serializer = FileWithAccessSerializer(files, many=True)
        return Response(file_serializer.data,)
