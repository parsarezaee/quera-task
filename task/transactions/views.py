from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from datetime import timedelta



class TransactionListAPIView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'category']

    def get_queryset(self):
        # Filter transactions based on the currently authenticated user
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the transaction with the currently authenticated user
        serializer.save(user=self.request.user)


class TransactionUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]


    def get_queryset(self):
        # Filter transactions based on the currently authenticated user
        return Transaction.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Ensure the transaction belongs to the authenticated user
        transaction = self.get_object()
        if transaction.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this transaction.")


class TransactionDeleteAPIView(generics.DestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]


    def get_queryset(self):
        # Filter transactions based on the currently authenticated user
        return Transaction.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        # Ensure the transaction belongs to the authenticated user
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this transaction.")


class CashFlowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, *args, **kwargs):
        # Get the specified date from query parameters
        date_string = request.query_params.get('date')

        # Parse the specified date into a datetime object
        try:
            specified_date = datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=400)

        # Calculate the start and end dates for the specified month
        start_date = specified_date.replace(day=1)
        if specified_date.month == 12:
            end_date = specified_date.replace(day=1, year=specified_date.year + 1) - timedelta(days=1)
        else:
            end_date = specified_date.replace(day=1, month=specified_date.month + 1) - timedelta(days=1)

        # Get the user's transactions for the specified month
        transactions = Transaction.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).order_by('date')

        # Serialize the transactions and return the response
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)