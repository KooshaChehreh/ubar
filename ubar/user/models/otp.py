from django.db import models
from user.validators import phone_validator
from django.utils.translation import gettext_lazy as _


class OTP(models.Model):
    code = models.IntegerField(
        verbose_name="کد یکبارمصرف",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="ایجاد شده در",
    )
    sent_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="ارسال پیامک در",
    )
    limited_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="محدود شده در",
    )
    phone = models.CharField(
        max_length=11,
        validators=[phone_validator],
        unique=True,
        verbose_name="تلفن همراه",
    )
    retries_count = models.IntegerField(
        default=0,
        verbose_name="تعداد تلاش برای وریفای ناموفق",
    )


    class Meta:
        verbose_name = "کد یکبارمصرف"
        verbose_name_plural = "کدهای یکبارمصرف"
        ordering = ["-id"]
