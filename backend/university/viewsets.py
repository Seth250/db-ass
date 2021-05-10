from rest_framework import viewsets, permissions
from .serializers import (
	FacultySerializer, 
	DepartmentSerializer,
	CourseSerializer, 
	StudentSerializer,
	ScoreSerializer
)
from .models import Faculty, Department, Course, Student, Score


class FacultyViewSet(viewsets.ModelViewSet):
	serializer_class = FacultySerializer
	permissions_classes = (permissions.IsAdminUser, )

	def get_queryset(self):
		return Faculty.objects.all()


class DepartmentViewSet(viewsets.ModelViewSet):
	serializer_class = DepartmentSerializer
	permissions_classes = (permissions.IsAdminUser, )
	lookup_field = 'slug'

	def get_queryset(self):
		return Department.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
	serializer_class = CourseSerializer
	permission_classes = (permissions.IsAdminUser, )
	lookup_field = 'code'

	def get_queryset(self):
		return Course.objects.all()


class StudentViewSet(viewsets.ModelViewSet):
	serializer_class = StudentSerializer
	permission_classes = (permissions.AllowAny, )
	# lookup_url_kwarg = 'matric_number'
	lookup_field = 'matric_number'

	def get_queryset(self):
		return Student.objects.all()


# class ScoreViewSet(viewsets.ModelViewSet):
# 	serializer_class = ScoreSerializer
# 	permission_classes = (permissions.AllowAny, )

# 	def get_queryset(self):
# 		return Student.objects.all()