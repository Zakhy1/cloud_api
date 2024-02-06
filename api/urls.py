from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from api.views import FileEditDeleteView, FileViewSet

app_name = 'api'

# router = DefaultRouter()
# router.register(r'files', FileViewSet, basename='files')

urlpatterns = [
    # path('files/', FileViewSet.as_view()),
    # path('files/<file_id>/', FileEditDeleteView.as_view()),
    # path('', include(router.urls)),
    path('files/', FileViewSet.as_view({'get': 'list'})),
    path('files/<int:pk>/', FileViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
         name='detail')
]
