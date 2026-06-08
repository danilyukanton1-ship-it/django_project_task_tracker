from config.models import BaseModel
from django.db import models


class UniqueQueue(BaseModel):
    item = models.CharField(max_length=100, unique=True)
