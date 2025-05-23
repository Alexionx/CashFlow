# Generated by Django 5.1.7 on 2025-04-25 04:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_budget_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='budget',
            name='income_category',
            field=models.CharField(choices=[('salary', 'Зарплата'), ('bonus', 'Бонус'), ('freelance', 'Фріланс'), ('other', 'Інше')], default='salary', max_length=50),
        ),
    ]
