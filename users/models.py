from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User Model
    Inherit:
        AbstractUser
    Fields:
        avatar     : ImageField
        bio        : CharField
        permission : CharField
    """

    SUPER = "SUPER"
    STAFF = "STAFF"
    NORMAL = "NORMAL"

    PERMISSION_CHOICES = (
        (SUPER, "SUPER"),
        (STAFF, "STAFF"),
        (NORMAL, "NORMAL"),
    )

    avatar = models.ImageField(upload_to="avatars", default="default_avatar.png")
    bio = models.CharField(max_length=100, default="")
    permission = models.CharField(
        choices=PERMISSION_CHOICES, max_length=6, default=NORMAL
    )
