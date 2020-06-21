from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import Permission


class User(AbstractUser):
    """Custom User Model
    Inherit:
        AbstractUser
    Fields:
        avatar     : ImageField
        bio        : CharField
        permission : CharField
    Meta:
        db_table   : users
    """

    avatar = models.ImageField(upload_to="avatars", default="default_avatar.png")
    bio = models.CharField(max_length=100, default="")
    permission = models.CharField(
        choices=Permission.choices, max_length=6, default=Permission.NORMAL
    )

    class Meta:
        db_table = "users"
