from django.urls import path
from user.views import (
    login_obtain_otp,
    login_verify_password,
)

urlpatterns = [
    path("login/obtain-otp", login_obtain_otp, name="login-obtain-otp"),
    path("login/verify-password", login_verify_password, name="login-verify-password"),
]
