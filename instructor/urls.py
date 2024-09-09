from django.urls import path
from .views import *

app_name = 'instructor'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('course_form/', CourseCreateView.as_view(), name='course_form'),
    path('mark-assessment/', MarkAssessmentView.as_view(), name='mark_assessment'),
    path('course-detail-create', course_detail_create, name='course_detail'),
]