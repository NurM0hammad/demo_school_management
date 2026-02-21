from django.contrib import admin
from .models import Student, Teacher, Course, Attendance, Grade

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'year', 'enrollment_date']
    list_filter = ['year', 'enrollment_date']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['courses']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'qualification', 'hire_date']
    search_fields = ['first_name', 'last_name', 'email']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'teacher']
    list_filter = ['credits']
    search_fields = ['name', 'code']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'is_present']
    list_filter = ['date', 'course', 'is_present']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'assignment_name', 'grade', 'date']
    list_filter = ['grade', 'date']