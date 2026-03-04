import requests
from django.db.models import Sum
from transactions.models import Transaction
from .models import AIInsight
from django.conf import settings
import json
import re
from django.utils import timezone
from datetime import timedelta

def extract_json(text):
    # Remove markdown code blocks if present
    text = re.sub(r"```json|```", "", text).strip()

    # Find first { and last }
    start = text.find("{")
    end = text.rfind("}") + 1

    if start != -1 and end != -1:
        json_str = text[start:end]
        return json.loads(json_str)

    raise ValueError("No valid JSON found in AI response")

def generate_financial_data(user, month, year):
    transactions = Transaction.objects.filter(
        user=user,
        transaction_date__month=month,
        transaction_date__year=year,
        is_deleted=False
    )

    total_income = transactions.filter(type="income").aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expense = transactions.filter(type="expense").aggregate(
        total=Sum("amount")
    )["total"] or 0

    category_data = list(
        transactions.filter(type="expense")
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "net_savings": float(total_income - total_expense),
        "category_breakdown": category_data,
    }


def build_prompt(data):
    return f"""
You are a financial advisor AI.

Analyze this monthly financial data:

Total Income: ${data['total_income']}
Total Expense: ${data['total_expense']}
Net Savings: ${data['net_savings']}

Category Breakdown:
{data['category_breakdown']}

Return STRICTLY in JSON format:

{{
  "summary": "2-3 sentence financial summary",
  "risk_level": "Low/Medium/High",
  "recommendations": [
      "Recommendation 1",
      "Recommendation 2"
  ],
  "potential_savings": "$ amount per month"
}}
"""


def call_groq_api(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a financial AI assistant. Always respond ONLY in valid JSON. Do not include explanations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Groq API Error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]


def generate_ai_insight(user , month, year):

    thirty_minutes_ago = timezone.now() - timedelta(minutes=30)

    # Check if insight exists within last 30 minutes
    existing = AIInsight.objects.filter(
        user=user,
        created_at__gte=thirty_minutes_ago
    ).order_by('-created_at').first()

    if existing:
        return existing

    # Generate fresh
    financial_data = generate_financial_data(user, month, year)
    prompt = build_prompt(financial_data)

    ai_raw_response = call_groq_api(prompt)

    try:
        ai_data = extract_json(ai_raw_response)
    except Exception:
        return {
            "summary": "AI summary generation failed. Please try again.",
            "risk_level": "Unknown",
            "recommendations": [],
            "potential_savings": "N/A"
        }

    insight = AIInsight.objects.create(
        user=user,
        month=month,
        year=year,
        summary=ai_data["summary"],
        risk_level=ai_data["risk_level"],
        recommendations=ai_data["recommendations"],
        potential_savings=ai_data["potential_savings"],
    )

    return insight