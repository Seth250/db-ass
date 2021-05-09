# from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer


# Create your views here.

class UserAuthToken(ObtainAuthToken):
    	
	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'token': token.key,
			'email': user.email
		})


class UserLogoutAPIView(APIView):
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
