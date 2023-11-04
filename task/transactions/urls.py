from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('list/', views.TransactionListAPIView.as_view(), name='transaction_list'),
    path('update/<int:pk>/', views.TransactionUpdateAPIView.as_view(), name='transaction_update'),
    path('delete/<int:pk>/', views.TransactionDeleteAPIView.as_view(), name='transaction_delete')
]
