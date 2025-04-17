
from django.contrib import admin
from django.urls import path, include

from django.http import HttpResponse



urlpatterns = [
    # Admin
    path("ss-admin/", admin.site.urls),
    # Apps
    path("api/v1/accounts/", include("user.urls")),
]