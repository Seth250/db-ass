from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from .serializers import UserSerializer

class UserListRetreiveViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = UserSerializer
	permission_classes = (permissions.IsAuthenticated, )

	def get_queryset(self):
		return get_user_model().objects.all()