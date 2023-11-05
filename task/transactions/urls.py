from django.urls import path
from .views import *


urlpatterns = [
    path('list/', TransactionListAPIView.as_view(), name='transaction_list'),
    path('update/<int:pk>/', TransactionUpdateAPIView.as_view(), name='transaction_update'),
    path('delete/<int:pk>/', TransactionDeleteAPIView.as_view(), name='transaction_delete'),
    path('report/', CashFlowAPIView.as_view(), name='cash-flow')
]
