from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from django.core.exceptions import PermissionDenied



class TransactionListAPIView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter transactions based on the currently authenticated user
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the transaction with the currently authenticated user
        serializer.save(user=self.request.user)


class TransactionUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

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

    def get_queryset(self):
        # Filter transactions based on the currently authenticated user
        return Transaction.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        # Ensure the transaction belongs to the authenticated user
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this transaction.")
