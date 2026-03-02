from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency_preference = models.CharField(max_length=10, default="INR")
    timezone = models.CharField(max_length=50, default="Asia/Kolkata")