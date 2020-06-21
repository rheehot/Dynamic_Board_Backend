from django.contrib import admin
from posts.models import Post, PostVotedUser


@admin.register(Post)
class BoardAdmin(admin.ModelAdmin):
    """Register Board model at admin panel
    Inherit:
        admin.ModelAdmin
    Fields:
        list_filter    : Fields used to filter Board object in the list
        list_display   : Fields visible in Board object list
    """

    list_filter = ("board",)

    list_display = (
        "title",
        "board",
        "create_user",
        "upvote",
        "downvote",
        "created_at",
        "updated_at",
    )


@admin.register(PostVotedUser)
class PostVotedUserAdmin(admin.ModelAdmin):
    """Register PostVotedUser model at admin panel
    Inherit:
        admin.ModelAdmin
    Fields:
        list_filter    : Fields used to filter PostVotedUser object in the list
        list_display   : Fields visible in PostVotedUser object list
    """

    list_filter = ("is_upvoted",)
    list_display = (
        "__str__",
        "is_upvoted",
        "created_at",
        "updated_at",
    )
