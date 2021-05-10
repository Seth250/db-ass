from rest_framework import serializers
from .models import Faculty, Department, Course, Score, Student, StudentScore
from accounts.serializers import UserSerializer
from django.db import transaction
from django.contrib.auth import get_user_model


class FacultySerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='university:faculty-detail')

	class Meta:
		model = Faculty
		fields = ('id', 'url', 'name')


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='university:department-detail', lookup_field='slug')
	faculty = FacultySerializer()

	class Meta:
		model = Department
		fields = ('id', 'url', 'name', 'slug', 'faculty')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='university:course-detail', lookup_field='code')
	# department = DepartmentSerializer()
	department = serializers.StringRelatedField()

	class Meta:
		model = Course
		fields = ('id', 'url', 'code', 'title', 'department')


class ScoreSerializer(serializers.ModelSerializer):
	course = serializers.HyperlinkedRelatedField(
		view_name='university:course-detail', 
		queryset=Course.objects.all(),
		lookup_field='code'
	)

	class Meta:
		model = Score
		fields = ('course', 'score')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='university:student-detail', lookup_field='matric_number')
	user = UserSerializer()
	# department = DepartmentSerializer()
	department = serializers.HyperlinkedRelatedField(
		view_name='university:department-detail',
		queryset=Department.objects.all(),
		lookup_field='slug'
	)
	# courses = CourseSerializer(many=True)
	courses = serializers.HyperlinkedRelatedField(
		view_name='university:course-detail',
		queryset=Course.objects.all(),
		lookup_field='code',
		many=True
	)
	scores = ScoreSerializer(many=True)

	class Meta:
		model = Student
		fields = ('id', 'url', 'user', 'matric_number', 'department', 'courses', 'scores')

	@transaction.atomic
	def create(self, validated_data):
		user_data = validated_data.pop('user')
		user = get_user_model().objects.create_user(**user_data)
		courses = validated_data.pop('courses')
		scores_data = validated_data.pop('scores')
		scores = [Score.objects.get_or_create(**data)[0] for data in scores_data]
		student = Student.objects.create(user=user, **validated_data)
		student.courses.add(*courses)
		student.scores.add(*scores)
		return student

	@transaction.atomic
	def update(self, instance, validated_data):
		instance.department = validated_data.get('department', instance.department)
		courses = validated_data.get('courses', [])
		if courses:
			instance.courses.add(*courses)

		scores_data = validated_data.get('scores', [])
		if scores_data:
			scores = [Score.objects.get_or_create(**data)[0] for data in scores_data]
			instance.scores.add(*scores)
			
		return instance
