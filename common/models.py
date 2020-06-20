from django.db import models


class AbstractTimeStamp(models.Model):
    """Abstract TimeStamp Model
    Inherit:
        Model
    Fields:
        created_at : DateTimeField (UnEditable)
        updated_at : DateTimeField (Editable)
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Permission(models.TextChoices):
    """Permission Choices Class
    Choices:
        SUPER  : Super user
        STAFF  : Staff user
        NORMAL : Normal user
    """

    SUPER = "Super"
    STAFF = "Staff"
    NORMAL = "Normal"
