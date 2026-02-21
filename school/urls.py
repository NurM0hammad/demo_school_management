from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Student URLs
    path('students/', views.student_list, name='student-list'),
    path('students/<int:pk>/', views.student_detail, name='student-detail'),
    path('students/create/', views.student_create, name='student-create'),
    path('students/<int:pk>/update/', views.student_update, name='student-update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student-delete'),
    
    # Teacher URLs
    path('teachers/', views.teacher_list, name='teacher-list'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher-detail'),
    path('teachers/create/', views.teacher_create, name='teacher-create'),
    
    # Course URLs
    path('courses/', views.course_list, name='course-list'),
    path('courses/<int:pk>/', views.course_detail, name='course-detail'),
    path('courses/create/', views.course_create, name='course-create'),
    
    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance-list'),
    path('attendance/create/', views.attendance_create, name='attendance-create'),
    
    # Grade URLs
    path('grades/', views.grade_list, name='grade-list'),
    path('grades/create/', views.grade_create, name='grade-create'),
]