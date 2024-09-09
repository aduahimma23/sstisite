from django.urls import path
from .views import *

app_name = 'student'

urlpatterns = [
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('course/<int:course_id>/feedback/', submit_feedback, name='submit_feedback'),
    path('attempt-assignment/<int:assignment_id>/', attempt_assignment, name='attempt_assignment'),
    path('course/<int:course_id>/request-certificate/', certificate_request, name='request_certificate'),
    path('certificate/<int:cert_id>/download/', download_certificate, name='download_certificate'),
]
