from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import FilesViewSet

router = SimpleRouter()
router.register(r'files', FilesViewSet, basename='files')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
]
urlpatterns += router.urls

