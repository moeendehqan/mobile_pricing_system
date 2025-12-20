from django.urls import path, include
from rest_framework import routers
from .views import transactionsView, BalanceView

urlpatterns = [
    path('transactions/', transactionsView.as_view()),
    path('balance/', BalanceView.as_view()),
]