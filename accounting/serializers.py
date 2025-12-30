from rest_framework import serializers
from .models import transactions


class transactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactions
        fields = '__all__'  


class TransactionInputSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    
    
