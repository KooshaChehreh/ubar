
from django.contrib import admin
from django.urls import path, include

from django.http import HttpResponse



urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Apps
    path("user/", include("user.urls")),
]