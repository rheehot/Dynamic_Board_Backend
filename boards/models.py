from django.db import models
from common.models import AbstractTimeStamp, Permission
from re import sub


class Board(AbstractTimeStamp):
    """Board Model
    Inherit:
        AbstractTimeStamp
    Fields:
        path             : CharField (PK)
        name             : CharField
        write_permission : CharField
        create_user      : User model (1:N)
    Methods:
        __str__          : Return board's name
        post_count       : Return related post counts
        save             : Remove special character in path
    Meta:
        db_table         : boards
    """

    name = models.CharField(max_length=60)
    path = models.CharField(max_length=20, primary_key=True)
    write_permission = models.CharField(
        choices=Permission.choices, max_length=6, default=Permission.NORMAL
    )
    create_user = models.ForeignKey(
        "users.User", related_name="boards", on_delete=models.CASCADE
    )

    def post_count(self):
        return len(self.posts.all())

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.path = sub(r"\W+", "", self.path)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "boards"
