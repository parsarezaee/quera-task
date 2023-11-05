from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from .models import Transaction
from .serializers import TransactionSerializer
from datetime import datetime


User = get_user_model()


class TransactionListAPIViewTest(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

    def test_list_transactions(self):
        Transaction.objects.create(user=self.user, amount=100.0, type='income', category='Bank', date='2023-11-01')
        Transaction.objects.create(user=self.user, amount=50.0, type='expense', category='Groceries', date='2023-11-02')

        
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')

        
        url = reverse('transaction_list')
        response = self.client.get(url)

        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
        expected_data = TransactionSerializer(Transaction.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_create_transaction(self):
        
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')

        
        url = reverse('transaction_list')
        data = {
            'user': self.user.id,
            'amount': 75.0, 
            'type': 'income', 
            'category': 'Bank', 
            'date': "2023-11-03"
            }
        response = self.client.post(url, data, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
        self.assertEqual(Transaction.objects.count(), 1)

        expected_date = datetime.strptime('2023-11-03', '%Y-%m-%d').date()

        
        self.assertEqual(Transaction.objects.get().amount, 75.0)
        self.assertEqual(Transaction.objects.get().type, 'income')
        self.assertEqual(Transaction.objects.get().category, 'Bank')
        self.assertEqual(Transaction.objects.get().date, expected_date)
        self.assertEqual(Transaction.objects.get().user, self.user)


class CashFlowAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.transaction_1 = Transaction.objects.create(
            user=self.user, amount=100.0, type='income', category='Salary', date='2023-11-01'
        )
        self.transaction_2 = Transaction.objects.create(
            user=self.user, amount=50.0, type='expense', category='Groceries', date='2023-11-15'
        )
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

    def test_cash_flow_api(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')
        date_param = '2023-11-01'
        url = reverse('cash-flow') + f'?date={date_param}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        start_date = datetime(2023, 11, 1)
        end_date = datetime(2023, 11, 30)
        expected_transactions = Transaction.objects.filter(
            user=self.user,
            date__range=[start_date, end_date]
        ).order_by('date')
        expected_data = TransactionSerializer(expected_transactions, many=True).data
        self.assertEqual(response.data, expected_data)
