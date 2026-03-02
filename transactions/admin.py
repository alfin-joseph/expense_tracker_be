from django.contrib import admin
from .models import Category, Transaction, RecurringTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "user", "is_default", "created_at")
    list_filter = ("type", "is_default")
    search_fields = ("name", "user__username")
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "type",
        "category",
        "transaction_date",
        "is_deleted",
    )
    list_filter = ("type", "transaction_date")
    search_fields = ("user__username", "description")
    ordering = ("-transaction_date",)
    
@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "type",
        "frequency",
        "next_run_date",
        "is_active",
    )
    list_filter = ("frequency", "is_active")
    search_fields = ("user__username",)