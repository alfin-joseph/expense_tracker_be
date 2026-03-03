import uuid
from django.db import models
from django.conf import settings


class AIInsight(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()

    summary = models.TextField()
    risk_level = models.CharField(max_length=20)
    recommendations = models.JSONField(default=list)
    potential_savings = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "month", "year")