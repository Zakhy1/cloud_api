from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from api.views import FilesViewSet

app_name = 'api'

# router = SimpleRouter()
# router.register(r'files', FilesViewSet, basename='files')
#
# urlpatterns = [
#     # path('files/', FileViewSet.as_view({'get': 'list', 'post': 'create'})),
#     # path('files/<int:pk>/', FileViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
#     #      name='detail')
# ]
# urlpatterns += router.urls
