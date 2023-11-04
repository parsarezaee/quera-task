from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=100)
    date = models.DateField()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.type == 'income':
            self.user.balance += self.amount
        elif self.type == 'expense':
            self.user.balance -= self.amount
        self.user.save()

    def __str__(self):
        return f"{self.user.username}'s {self.type} transaction of ${self.amount} on {self.date}"
