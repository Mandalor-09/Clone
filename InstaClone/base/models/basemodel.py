from django.db import models
from uuid import uuid4

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid4)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True