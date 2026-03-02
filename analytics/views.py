from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Avg
from django.db.models.functions import ExtractMonth
from transactions.models import Transaction
from datetime import datetime


class AnalyticsOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        period = request.query_params.get("period", "monthly")
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        queryset = Transaction.objects.filter(
            user=user,
            is_deleted=False
        )

        if month and year:
            queryset = queryset.filter(
                transaction_date__month=month,
                transaction_date__year=year
            )

        # Totals
        total_income = queryset.filter(type="income").aggregate(
            total=Sum("amount")
        )["total"] or 0

        total_expense = queryset.filter(type="expense").aggregate(
            total=Sum("amount")
        )["total"] or 0

        # Average monthly (based on all time)
        avg_income = (
            Transaction.objects.filter(user=user, type="income")
            .values("transaction_date__year", "transaction_date__month")
            .annotate(monthly_total=Sum("amount"))
            .aggregate(avg=Avg("monthly_total"))["avg"]
            or 0
        )

        avg_expense = (
            Transaction.objects.filter(user=user, type="expense")
            .values("transaction_date__year", "transaction_date__month")
            .annotate(monthly_total=Sum("amount"))
            .aggregate(avg=Avg("monthly_total"))["avg"]
            or 0
        )

        # Trend data (monthly grouping)
        trend_data = (
            Transaction.objects.filter(user=user)
            .annotate(month=ExtractMonth("transaction_date"))
            .values("month", "type")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        # Category distribution
        category_distribution = (
            queryset.filter(type="expense")
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        return Response({
            "summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "net_savings": total_income - total_expense,
                "avg_monthly_income": avg_income,
                "avg_monthly_expense": avg_expense,
            },
            "trend": trend_data,
            "category_distribution": category_distribution,
        })