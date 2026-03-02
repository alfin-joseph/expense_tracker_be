import django_filters
from .models import Transaction
from datetime import datetime

class TransactionFilter(django_filters.FilterSet):
    month = django_filters.NumberFilter(method="filter_by_month")
    year = django_filters.NumberFilter(method="filter_by_year")

    class Meta:
        model = Transaction
        fields = ["type", "category"]

    def filter_by_month(self, queryset, name, value):
        return queryset.filter(transaction_date__month=value)

    def filter_by_year(self, queryset, name, value):
        return queryset.filter(transaction_date__year=value)
    
    
        