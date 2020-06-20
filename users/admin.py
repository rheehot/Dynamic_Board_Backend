from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Register User model at admin panel
    Set fieldsets BaseUserAdmin's fieldsets + user_fieldsets

    Inherit:
        UserAdmin as BaseUserAdmin
    Fields:
        user_fieldsets : Custom User model's fieldsets
        fieldsets      : Fields visible in User object detail
        list_filter    : Fields used to filter User object in the list
        list_display   : Fields visible in User object list
    """

    user_fieldsets = (("Custom Profile", {"fields": ("avatar", "permission")},),)
    fieldsets = BaseUserAdmin.fieldsets + user_fieldsets

    list_filter = BaseUserAdmin.list_filter + ("permission",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "last_login",
        "permission",
        "is_active",
    )
