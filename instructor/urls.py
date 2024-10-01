from django.urls import path
from .views import *

app_name = 'instructor'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('course_form/', CourseCreateView.as_view(), name='course_form'),
    path('mark-assessment/', MarkAssessmentView.as_view(), name='mark_assessment'),
    path('course-detail-create', course_detail_create, name='course_detail'),
    path('course/<int:course_id>/students/', student_enrolled, name='enrolled_students'),
    path('assignments/', assignment_list, name='assignment_list'),
    path('assignments/create/', create_assignment, name='create_assignment'),
    path('assignments/<int:assignment_id>/edit/', edit_assignment, name='edit_assignment'),
    path('assignments/<int:assignment_id>/delete/', delete_assignment, name='delete_assignment'),
]