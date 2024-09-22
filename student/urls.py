from django.urls import path
from .views import *

app_name = 'student'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('course/', course_list, name='course'),
    path('profile/', student_profile, name='student_profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('course/<str:course_id>/', course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('course/<int:course_id>/feedback/', submit_feedback, name='submit_feedback'),
    path('course/<int:course_id>/request-certificate/', certificate_request, name='request_certificate'),
    path('certificate/<int:cert_id>/download/', download_certificate, name='download_certificate'),
    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/add/<int:course_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:course_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('favorites/add/<int:course_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:course_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', favorite_list, name='favorite_list'),
    path('submit-assessment/<int:assessment_id>/', submit_assessment, name='submit_assessment'),
    path('assessment-results/<int:attempt_id>/', assessment_results, name='assessment_results'),
]
