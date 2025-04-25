from django.utils import timezone
from django.db import models

class Budget(models.Model):
    INCOME_CATEGORIES = [
        ('salary', 'Зарплата'),
        ('bonus', 'Бонус'),
        ('freelance', 'Фріланс'),
        ('other', 'Інше'),
    ]
    
    income = models.DecimalField(max_digits=10, decimal_places=2)
    income_category = models.CharField(max_length=50, choices=INCOME_CATEGORIES, default='salary')
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.balance = self.income - self.expenses
        if not self.date:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_income_category_display()}: {self.income} грн ({self.date})"


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
