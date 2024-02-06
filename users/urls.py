from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


from users.views import RegisterView, DeleteAuthToken, GetAuthToken

app_name = 'users'

urlpatterns = [
    path('drf-auth/', include('rest_framework.urls')),
    path('login/', GetAuthToken.as_view(), name='api_token_auth'),
    path('logout/', DeleteAuthToken.as_view()),
    path('register/', RegisterView.as_view())
]
