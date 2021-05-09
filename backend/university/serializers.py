from rest_framework import serializers
from .models import Student
from accounts.serializers import UserSerializer
from django.db import transaction
from django.contrib.auth import get_user_model


class StudentSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField()
	user = UserSerializer()

	class Meta:
		model = Student
		fields = ('id', 'user', 'matric_number', 'department', 'faculty', 'courses')

	@transaction.atomic
	def create(self, validated_data):
		user_data = validated_data.pop('user')
		user = get_user_model().objects.create_user(**user_data)
		student = Student.objects.create(user=user, **validated_data)
		return student