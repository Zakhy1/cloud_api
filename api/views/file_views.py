import uuid

from django.http import FileResponse

from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets

from api.models import File, User, Access
from cloud_api.generics.common import response_error
from cloud_api.generics.permissions import CustomIsOwner
from api.serializers.file_serializers import FileSerializer, UploadedFileSerializer, FileWithAccessSerializer, \
    AccessSerializer


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
            Access.objects.create(user=request.user, file=uploaded_file, author=True)
            host = 'http://127.0.0.1:8000'
            uploaded_files.append({  # TODO serializer
                'success': True,
                'message': 'Success',
                'name': uploaded_file.name,
                'url': f'{host}/files/{uploaded_file.file_id}',
                'file_id': uploaded_file.file_id
            })
            return Response(uploaded_files, status=status.HTTP_201_CREATED)
        return response_error(serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['pk'])
        if file.owner == request.user:  # TODO check without
            return FileResponse(open(file.file.path, 'rb'))
        raise PermissionDenied(detail='Forbidden for you', code=403)

    def update(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['pk'])
        file.name = request.data['name']
        file.save()
        if file.owner == request.user:
            return Response({
                'success': True,
                'message': 'Renamed'
            })
        raise PermissionDenied(detail='Forbidden for you', code=403)

    def destroy(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['pk'])
        file.delete()
        return Response({
            'success': True,
            'message': 'File already deleted',
        })

    @action(methods=('post', 'delete'), detail=True, url_path='accesses')
    def manage_access(self, request, *args, **kwargs):

        try:
            user = User.objects.get(email=request.data['email'])
            user.co_author = True
        except User.DoesNotExist:
            raise ValidationError(detail={'message': 'Enter the correct user email'}, code=422)
        if request.method == 'POST':
            file = get_object_or_404(File, pk=kwargs['pk'])
            if request.user != file.owner:
                raise PermissionDenied(detail='Forbidden for you', code=403)
            Access.objects.get_or_create(user=user, file=file)
            serializer = AccessSerializer(file.accesses, many=True)
            return Response(serializer.data)

        if request.method == 'DELETE':
            access = Access.objects.get(user__email=user.email)
            file = access.file
            serializer = AccessSerializer(file.accesses, many=True)
            access.delete()
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
        return Response(file_serializer.data, )
