from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views.file_views import FilesViewSet
from api.views.user_views import GetAuthToken, DeleteAuthToken, RegisterView

router = SimpleRouter()
router.register(r'files', FilesViewSet, basename='files')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('drf-auth/', include('rest_framework.urls')),
    path('login/', GetAuthToken.as_view(), name='api_token_auth'),
    path('logout/', DeleteAuthToken.as_view()),
    path('register/', RegisterView.as_view())
]
urlpatterns += router.urls
