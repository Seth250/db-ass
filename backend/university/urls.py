from django.urls import path, include
from .viewsets import (
	FacultyViewSet,
	DepartmentViewSet,
	CourseViewSet,
	StudentViewSet,
	ScoreViewSet
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'faculties', FacultyViewSet, basename='faculty')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'scores', ScoreViewSet, basename='score')

app_name = 'university'

urlpatterns = [
	path('', include(router.urls))
]