from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Faculty(models.Model):
	name = models.CharField(max_length=75)

	class Meta:
		verbose_name_plural = 'faculties'

	def __str__(self):
		return self.name


class Department(models.Model):
	name = models.CharField(max_length=75)
	slug = models.SlugField(default='', max_length=75, editable=False, unique=True)
	faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify('%s' % self.name, allow_unicode=True)
		return super(Department, self).save(*args, **kwargs)


class Course(models.Model):
	code = models.CharField(max_length=10, unique=True)
	title = models.CharField(max_length=50)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

	def __str__(self):
		return self.code


class Score(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='scores')
	score = models.PositiveIntegerField(default=0)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['course', 'score'], name='unique_course_score'),
		]

	def __str__(self):
		return '%s in %s' % (self.score, self.course)


class Student(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	matric_number = models.PositiveIntegerField(unique=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
	# faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students')
	courses = models.ManyToManyField(Course, related_name='students')
	scores = models.ManyToManyField(Score, related_name='students', through='StudentScore')

	def __str__(self):
		return '%d' % self.matric_number


class StudentScore(models.Model):
	score = models.ForeignKey(Score, on_delete=models.CASCADE, related_name='student_scores')
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_scores')

	def __str__(self):
		return '%s scored %s' % (self.student, self.score)

	def clean(self, *args, **kwargs):
		if self.score_id and self.score.course_id:
			if self.__class__.objects.filter(student=self.student, score__course=self.score.course).exists():
				raise exceptions.ValidationError(
					_('Instance of StudentScore with student and score.course already exists.'),
					code='unique_together',
				)


# class Student(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# 	matric_number = models.PositiveIntegerField(unique=True)
# 	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
# 	# faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students')
# 	courses = models.ManyToManyField(Course, related_name='students')
# 	scores = models.ManyToManyField(Score, related_name='students')

# 	def __str__(self):
# 		return '%d' % self.matric_number
