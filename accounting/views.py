from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import transactions
from .serializers import transactionsSerializer
from rest_framework.response import Response
from django.db.models import Sum



# Create your views here.
class transactionsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        transactions = transactions.objects.filter(user=request.user)
        serializer = transactionsSerializer(transactions, many=True)
        return Response(serializer.data)


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        balance = transactions.objects.filter(user=request.user).aggregate(Sum('bede'), Sum('best'))
        balance['bede'] = balance['bede__sum'] or 0
        balance['best'] = balance['best__sum'] or 0
        return Response(balance)
