from django.contrib import admin
from boards.models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Register Board model at admin panel
    Inherit:
        admin.ModelAdmin
    Fields:
        list_filter    : Fields used to filter Board object in the list
        list_display   : Fields visible in Board object list
    """

    list_filter = ("write_permission",)

    list_display = (
        "name",
        "path",
        "write_permission",
        "create_user",
        "created_at",
        "updated_at",
    )
