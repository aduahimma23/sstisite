from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('contact/', contact_view, name='contact')
]