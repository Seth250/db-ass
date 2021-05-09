from rest_framework import serializers
from .models import Faculty, Department, Course, Student, Score
from accounts.serializers import UserSerializer
from django.db import transaction
from django.contrib.auth import get_user_model


class FacultySerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='university:faculty-detail')

	class Meta:
		model = Faculty
		fields = ('id', 'url', 'name')


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='university:department-detail')
	faculty = FacultySerializer()

	class Meta:
		model = Department
		fields = ('id', 'url', 'name', 'faculty')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='university:course-detail')
	# department = DepartmentSerializer()
	department = serializers.StringRelatedField()

	class Meta:
		model = Course
		fields = ('id', 'url', 'code', 'title', 'department')


class ScoreSerializer(serializers.ModelSerializer):
	course = serializers.StringRelatedField()

	class Meta:
		model = Score
		fields = ('course', 'score')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='university:student-detail')
	user = UserSerializer()
	department = DepartmentSerializer()
	courses = CourseSerializer(many=True)
	scores = ScoreSerializer(many=True)

	class Meta:
		model = Student
		fields = ('id', 'url', 'user', 'matric_number', 'department', 'courses', 'scores')

	@transaction.atomic
	def create(self, validated_data):
		user_data = validated_data.pop('user')
		user = get_user_model().objects.create_user(**user_data)
		student = Student.objects.create(user=user, **validated_data)
		return student
