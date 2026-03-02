import uuid
from django.db import models
from django.conf import settings

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)
    color = models.CharField(max_length=20, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.name} ({self.type})"
    
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    description = models.TextField(blank=True, null=True)

    transaction_date = models.DateField()

    is_recurring = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)  # Soft delete

    class Meta:
        ordering = ["-transaction_date"]
        indexes = [
            models.Index(fields=["user", "transaction_date"]),
            models.Index(fields=["user", "type"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.type}"
    

class RecurringTransaction(models.Model):
    FREQUENCY_CHOICES = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("weekly", "Weekly"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    type = models.CharField(max_length=10, choices=Transaction.TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)

    next_run_date = models.DateField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)