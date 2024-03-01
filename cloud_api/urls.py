from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views.file_views import FilesViewSet
from api.views.user_views import UserViewSet

router = SimpleRouter()
router.register(r'files', FilesViewSet, basename='files')
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += router.urls
