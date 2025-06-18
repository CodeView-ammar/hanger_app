from django.shortcuts import render
from rest_framework import viewsets, status
from users.models import Users
# Create your views here.
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transaction
from django.db.models import Sum
from rest_framework.views import APIView

class TransactionCreateAPIView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class WalletView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({"error": "user_id مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({"error": "المستخدم غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        # احتساب الرصيد: مجموع الدائن - مجموع المدين
        credit_total = Transaction.objects.filter(user=user).aggregate(Sum('credit'))['credit__sum'] or 0
        debit_total = Transaction.objects.filter(user=user).aggregate(Sum('debit'))['debit__sum'] or 0
        balance = credit_total - debit_total

        # جلب جميع العمليات الخاصة بالمستخدم
        transactions = Transaction.objects.filter(user=user).order_by('-date')
        serializer = TransactionSerializer(transactions, many=True)

        return Response({
            "balance": balance,
            "transactions": serializer.data
        })