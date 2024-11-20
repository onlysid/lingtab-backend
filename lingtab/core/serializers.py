from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'user_id', 'amount', 'description', 'date', 'repayment']
        read_only_fields = ['id', 'date']