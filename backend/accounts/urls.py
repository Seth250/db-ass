from django.urls import path, include
from .views import UserAuthToken, UserLogoutAPIView
from .viewsets import UserListRetreiveViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserListRetreiveViewSet, basename='user')

app_name = 'accounts'

urlpatterns = [
	path('', include(router.urls)),
	path('auth/token/login/', UserAuthToken.as_view(), name='user-auth-token'),
	path('auth/token/logout', UserLogoutAPIView.as_view(), name='user-logout')
]