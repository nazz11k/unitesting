from django.urls import path

from app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('courses/<int:pk>/lecture/create/', LectureCreateView.as_view(), name='lecture_create'),
    path('lectures/<int:pk>/', LectureDetailView.as_view(), name='lecture_detail'),
    path('lectures/<int:pk>/delete/', LectureDeleteView.as_view(), name='lecture_delete'),
    path('courses/<int:pk>/task/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
