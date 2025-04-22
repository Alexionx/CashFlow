from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class Budget(models.Model):
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Обчислюємо залишок бюджету як різницю між доходом і витратами
        self.balance = self.income - self.expenses
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Бюджет: {self.income} грн, Витрати: {self.expenses} грн, Залишок: {self.balance} грн"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Харчування'),
        ('transport', 'Транспорт'),
        ('entertainment', 'Розваги'),
        ('other', 'Інше'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    time_added = models.DateTimeField(auto_now_add=True)  # Точний час додавання витрати

    def __str__(self):
        return f"{self.category} - {self.amount} грн"
