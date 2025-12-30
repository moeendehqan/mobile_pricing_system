from django.urls import path, include
from rest_framework import routers
from .views import transactionsView, BalanceView, CreateTransactionView, VerifyTransactionView



urlpatterns = [
    path('transactions/', transactionsView.as_view()),
    path('balance/', BalanceView.as_view()),
    path('create/', CreateTransactionView.as_view()),
    path('verify/', VerifyTransactionView.as_view()),
]