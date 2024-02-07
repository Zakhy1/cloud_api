import uuid

from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import File
from api.serializers import FileSerializer, UploadedFileSerializer, FileToUserSerializer
from cloud_api.permissions import CustomIsOwner


class FileViewSet(viewsets.ViewSet):
    permission_classes = [CustomIsOwner]


    def list(self, request):
        queryset = File.objects.filter(owner=request.user)
        serializer = UploadedFileSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.initial_data['files']
            uploaded_files = []

            uploaded_file = File.objects.create(name=file.name, file_id=uuid.uuid4(),
                                                owner=request.user,
                                                file=file)
            uploaded_files.append({
                'success': True,
                'message': 'Success',
                'name': uploaded_file.name,
                'url': f'{{host}}/files/{uploaded_file.file_id}',
                'file_id': uploaded_file.file_id
            })
            return Response(uploaded_files, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        try:
            file = File.objects.get(id=pk)
        except Exception:
            raise NotFound(detail=None, code=404)

        return FileResponse(open(file.file.path, 'rb'))

    def update(self, request, pk=None):
        try:
            file = File.objects.get(id=pk)
        except Exception:
            return Response({'message': 'not found'}, status=404)
        file.name = request.data['name']
        file.save()
        return Response({
            'success': True,
            'message': 'Renamed'
        })

    def destroy(self, request, pk=None):
        try:
            file = File.objects.get(id=pk)
        except Exception:
            return Response({'message': 'not found'}, status=404)

        file.delete()
        return Response({
            'success': True,
            'message': 'File already deleted',
        })
