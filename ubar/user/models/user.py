import logging
import jwt
from django.db import models
from django.conf import settings
from user.validators import phone_validator, national_code_validator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.utils import timezone




class User(models.Model):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name="نام",
    )
    family = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="نام خانوادگی",
    )
    phone = models.CharField(
        max_length=11,
        validators=[phone_validator],
        verbose_name="تلفن همراه",
    )

    password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="پسورد",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="ایجاد شده در"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="بروز شده در")
    limited_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("محدود شده در")
    )
    suspended_at = models.DateTimeField(
        blank=True, null=True, verbose_name="تاریخ تعلیق"
    )

    @classmethod
    def get_or_create_user(cls, phone: str):
        # !TODO(alireza) important: when creating new user, also set a field to know who has created this
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return User.objects.create(phone=phone)

    @staticmethod
    def from_request(request, anonymous_raise_401=False):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            if anonymous_raise_401:
                raise AuthenticationFailed
            else:
                return None
        try:
            access_token = auth_header.split(" ")[1]
            payload = jwt.decode(
                jwt=access_token,
                key=settings.LOADED_JWT_PUBLIC_KEY,
                algorithms=["RS256"],
            )
        except (jwt.exceptions.DecodeError, jwt.exceptions.DecodeError):
            raise AuthenticationFailed(
                detail={"message": "Invalid token", "code": "invalid_token"}
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                detail={"message": "Expired token", "code": "token_expired"}
            )

    def hash_password(self, raw_password):
        self.password = make_password(password=raw_password)

    def check_password(self, entered_password):
        if bool(self.password):
            return check_password(password=entered_password, encoded=self.password)
        else:
            return False

    def delete(self, *args, **kwargs):
        if self.suspended_at is None:
            self.suspended_at = timezone.now()
            self.save()

    def hard_delete(self, *args, **kwargs):
        super(User, self).delete(*args, **kwargs)

    def is_suspended(self):
        return self.suspended_at is not None


    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-id"]

    