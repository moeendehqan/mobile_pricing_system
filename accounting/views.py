from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import transactions
from .serializers import transactionsSerializer
from rest_framework.response import Response
from django.db.models import Sum
from .serializers import TransactionInputSerializer
from core.services.zarinpal import ZarinpalService
from django.http import HttpResponseRedirect



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
        balance = transactions.objects.filter(user=request.user, is_confirmed=True).aggregate(Sum('bede'), Sum('best'))
        balance['bede'] = balance['bede__sum'] or 0
        balance['best'] = balance['best__sum'] or 0
        return Response(balance)



class CreateTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = TransactionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        amount = serializer.validated_data['amount']
        zarinpal = ZarinpalService()
        response = zarinpal.create(
            amount=amount,
            user=request.user
        )
        if not response:
            return Response({'error': 'خطا در اتصال به درگاه پرداخت'}, status=400)
        return Response(response, status=201)



class VerifyTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        status = request.GET.get('Status').lower()
        authority = request.GET.get('Authority')
        if status != "ok":
            return HttpResponseRedirect('https://panel.shikala.com/accounting?status=failed')
        zarinpal = ZarinpalService()
        response = zarinpal.verify(
            authority=authority
        )
        if not response:
            return HttpResponseRedirect('https://panel.shikala.com/accounting?status=failed')
        return HttpResponseRedirect('https://panel.shikala.com/accounting?status=success')
