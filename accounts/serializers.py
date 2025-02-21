from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'date', 'date_jsut', 'transaction_type', 'amount', 'debit', 'credit', 'description']