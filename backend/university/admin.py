from django.contrib import admin
from .models import Student, Score, StudentScore, Course, Department, Faculty

# Register your models here.

admin.site.register(Student)
admin.site.register(Score)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(StudentScore)