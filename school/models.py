from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    qualification = models.CharField(max_length=100)
    hire_date = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='teachers/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('teacher-detail', args=[str(self.id)])

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    credits = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='courses')

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse('course-detail', args=[str(self.id)])

class Student(models.Model):
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, default='1')
    courses = models.ManyToManyField(Course, related_name='students', blank=True)
    photo = models.ImageField(upload_to='students/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'course', 'date']

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date}"

class Grade(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    assignment_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.assignment_name}: {self.grade}"