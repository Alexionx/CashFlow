from django.db import models

# Create your models here.
from django.db import models

class Budget(models.Model):
    income = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.income} грн"
