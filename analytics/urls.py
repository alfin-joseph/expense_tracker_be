from django.urls import path
from .views import AnalyticsOverviewView
from .views import AISummaryView

urlpatterns = [
    path("overview/", AnalyticsOverviewView.as_view(), name="analytics-overview"),
    path("ai-summary/", AISummaryView.as_view(), name="ai-summary"),
]