from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import Student, Teacher, Course, Attendance, Grade
from .forms import (StudentForm, TeacherForm, CourseForm, AttendanceForm, 
                   GradeForm, UserRegistrationForm)

def home(request):
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    course_count = Course.objects.count()
    
    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'course_count': course_count,
        'recent_students': Student.objects.all().order_by('-enrollment_date')[:5],
        'recent_teachers': Teacher.objects.all().order_by('-hire_date')[:5],
    }
    return render(request, 'school/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'school/registration/register.html', {'form': form})

# Student Views
def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        students = Student.objects.all()
    return render(request, 'school/student_list.html', {'students': students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendances = Attendance.objects.filter(student=student).order_by('-date')[:10]
    grades = Grade.objects.filter(student=student).order_by('-date')[:10]
    return render(request, 'school/student_detail.html', {
        'student': student,
        'attendances': attendances,
        'grades': grades
    })

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Student created successfully!')
            return redirect('student-detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'school/student_form.html', {'form': form, 'title': 'Add Student'})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student-detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'school/student_form.html', {'form': form, 'title': 'Edit Student'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student-list')
    return render(request, 'school/student_confirm_delete.html', {'student': student})

# Teacher Views
def teacher_list(request):
    query = request.GET.get('q')
    if query:
        teachers = Teacher.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        teachers = Teacher.objects.all()
    return render(request, 'school/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    courses = Course.objects.filter(teacher=teacher)
    return render(request, 'school/teacher_detail.html', {'teacher': teacher, 'courses': courses})

@login_required
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, 'Teacher created successfully!')
            return redirect('teacher-detail', pk=teacher.pk)
    else:
        form = TeacherForm()
    return render(request, 'school/teacher_form.html', {'form': form, 'title': 'Add Teacher'})

# Course Views
def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(
            Q(name__icontains=query) | 
            Q(code__icontains=query)
        )
    else:
        courses = Course.objects.all()
    return render(request, 'school/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    students = course.students.all()
    return render(request, 'school/course_detail.html', {'course': course, 'students': students})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course-detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'school/course_form.html', {'form': form, 'title': 'Add Course'})

# Attendance Views
@login_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('attendance-list')
    else:
        form = AttendanceForm()
    return render(request, 'school/attendance_form.html', {'form': form})

@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'school/attendance_list.html', {'attendances': attendances})

# Grade Views
@login_required
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade recorded successfully!')
            return redirect('grade-list')
    else:
        form = GradeForm()
    return render(request, 'school/grade_form.html', {'form': form})

@login_required
def grade_list(request):
    grades = Grade.objects.all().order_by('-date')
    return render(request, 'school/grade_list.html', {'grades': grades})