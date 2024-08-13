from django.contrib import admin
from django.urls import path, include
from main.views import home_view
urlpatterns = [
    path('', home_view),
    path('main/', include('main.urls')),
    path("admin/", admin.site.urls),
]
