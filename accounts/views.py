from django.shortcuts import render
from rest_framework import viewsets, status

# Create your views here.
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionCreateAPIView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer