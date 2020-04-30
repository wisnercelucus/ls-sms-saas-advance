from django.contrib import admin
from django.urls import path, include
from school import views
from django.contrib.auth import views as auth_views

app_name = 'school'

urlpatterns = [
	path('', views.index, name='index'),
    path('students/all/', views.get_pupil_list, name='list_pupil'),
    path('students/new/', views.add_new_pupil, name='add_new_pupil'),
    path('students/<str:pk>/', views.get_detail_pupil, name='show_detail_pupil'),
    path('students/<str:pk>/edit/', views.update_pupil, name='update_pupil'),

	path('attendances/all/', views.get_attendance_list, name='list_attendance'),
	path('attendances/new/', views.add_new_attendance, name='add_new_attendance'),
	path('attendances/<str:pk>/', views.get_detail_attendance, name='show_detail_attendance'),
	path('attendances/<str:pk>/edit/', views.update_attendance, name='update_attendance'),

    path('courses/all/', views.get_course_list, name='list_course'),
    path('courses/new/', views.add_new_course, name='add_new_course'),
    path('courses/<str:pk>/', views.get_detail_course, name='show_detail_course'),
    path('courses/<str:pk>/edit/', views.update_course, name='update_course'),

    path('ExamMarks/all/', views.get_mark_list, name='list_mark'),
    path('ExamMarks/new/', views.add_new_mark, name='add_new_mark'),
    path('ExamMarks/<str:pk>/', views.get_detail_mark, name='show_detail_mark'),
    path('ExamMarks/<str:pk>/edit/', views.update_mark, name='update_mark'),

    path('teachers/all/', views.get_teacher_list, name='list_teacher'),
    path('teachers/new/', views.add_new_teacher, name='add_new_teacher'),
    path('teachers/<str:pk>/', views.get_detail_teacher, name='show_detail_teacher'),
    path('teachers/<str:pk>/edit/', views.update_teacher, name='update_teacher'),

    path('grades/all/', views.get_grade_list, name='list_grade'),
    path('grades/new/', views.add_new_grade, name='add_new_grade'),
    path('grades/<str:pk>/', views.get_detail_grade, name='show_detail_grade'),
    path('grades/<str:pk>/edit/', views.update_grade, name='update_grade'),

    path('terms/all/', views.get_term_list, name='list_term'),
    path('terms/new/', views.add_new_term, name='add_new_term'),
    path('terms/<str:pk>/', views.get_detail_term, name='show_detail_term'),
    path('terms/<str:pk>/edit/', views.update_term, name='update_term'),

    path('ac/all/', views.get_ac_list, name='list_ac'),
    path('ac/new/', views.add_new_ac, name='add_new_ac'),
    path('ac/<str:pk>/', views.get_detail_ac, name='show_detail_ac'),
    path('ac/<str:pk>/edit/', views.update_ac, name='update_ac'),

    path('responsibles/all/', views.get_responsible_list, name='list_responsible'),
    path('responsibles/new/', views.add_new_responsible, name='add_new_responsible'),
    path('responsibles/<str:pk>/', views.get_detail_responsible, name='show_detail_responsible'),
    path('responsibles/<str:pk>/edit/', views.update_responsible, name='update_responsible'),
]
