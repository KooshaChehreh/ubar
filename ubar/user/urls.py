from django.urls import path
from user.views import (
    login_obtain_otp,
    login_verify_password,
    profile,
    login_verify_otp
)

urlpatterns = [
    path("login/obtain-otp", login_obtain_otp, name="login-obtain-otp"),
    path("login/verify-password", login_verify_password, name="login-verify-password"),
    path("login/profile", profile, name="login-profile"),
    path("login/verify-otp", login_verify_otp, name="login-verify-otp"),

]
