from django.db import models
from django.conf import settings

# Create your models here.

class Faculty(models.Model):
	name = models.CharField(max_length=75)

	class Meta:
		verbose_name_plural = 'faculties'

	def __str__(self):
		return self.name


class Department(models.Model):
	name = models.CharField(max_length=75)
	faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

	def __str__(self):
		return self.name


class Course(models.Model):
	code = models.CharField(max_length=10, unique=True)
	title = models.CharField(max_length=50)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

	def __str__(self):
		return self.code


class Score(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	score = models.PositiveIntegerField(default=0)

	def __str__(self):
		return 'score: %s for %s' % (self.score, self.course)


class Student(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	matric_number = models.PositiveIntegerField(unique=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
	# faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students')
	courses = models.ManyToManyField(Course, related_name='students')
	scores = models.ManyToManyField(Score, related_name='students')

	def __str__(self):
		return '%d' % self.matric_number
