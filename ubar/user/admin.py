from django.contrib import admin
from user.models.user import User

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