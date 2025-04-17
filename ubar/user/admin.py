from django.contrib import admin
from user.models.user import User
from user.models.otp import OTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "family",
        "suspended_at",
        "phone",
        "created_at",
        "updated_at",
        "limited_at",
    ]
    list_filter = [
        "created_at",
    ]
    search_fields = ["name", "family", "phone", "id"]


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "phone",
        "code",
        "retries_count",
        "ip_address"
        "created_at",
        "sent_at",
        "limited_at",
    ]
    list_filter = [
        "created_at",
        "sent_at",
        "limited_at",
    ]
    search_fields = ["phone", "id"]