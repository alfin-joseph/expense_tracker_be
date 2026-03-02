from rest_framework import viewsets, permissions
from .models import Category, Transaction
from .serializers import (
    CategorySerializer,
    TransactionCreateSerializer,
    TransactionDetailSerializer,
)
from .filters import TransactionFilter
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TransactionFilter
    ordering_fields = ["transaction_date", "amount"]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user,
            is_deleted=False
        )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TransactionDetailSerializer
        return TransactionCreateSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
        
@action(detail=False, methods=["get"])
def monthly_summary(self, request):
    month = request.query_params.get("month")
    year = request.query_params.get("year")

    if not month or not year:
        return Response(
            {"error": "Month and year are required."},
            status=400
        )

    transactions = self.get_queryset().filter(
        transaction_date__month=month,
        transaction_date__year=year
    )

    income = transactions.filter(type="income").aggregate(
        total=Sum("amount")
    )["total"] or 0

    expense = transactions.filter(type="expense").aggregate(
        total=Sum("amount")
    )["total"] or 0

    category_breakdown = (
        transactions
        .values("category__name")
        .annotate(total=Sum("amount"))
    )

    return Response({
        "month": month,
        "year": year,
        "total_income": income,
        "total_expense": expense,
        "net_savings": income - expense,
        "category_breakdown": category_breakdown
    })