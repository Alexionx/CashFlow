from sqlite3 import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import BudgetForm
from .models import Budget, Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import logout

# Функція для реєстрації
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Отримуємо дані форми
                user = form.save(commit=False)  # Не зберігаємо ще користувача
                user.set_password(form.cleaned_data['password'])  # Хешуємо пароль
                user.save()  # Зберігаємо користувача з хешованим паролем
                login(request, user)  # Авторизуємо користувача після реєстрації
                return redirect('home')  # Перенаправлення на сторінку профілю
            except IntegrityError:
                # Якщо виникає помилка унікальності
                form.add_error('username', 'Користувач з таким ім\'ям вже існує!')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration.html', {'form': form})

# Функція для входу
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # редірект на домашню сторінку після входу
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Функція для профілю
@login_required
def profile(request):
    return render(request, 'profile.html')

# Інші функції
@login_required
def createPlan(request):
    return render(request, 'createPlan.html')

@login_required
def chart(request):
    return render(request, 'chart.html')

@login_required
def costs(request):
    return HttpResponse('<h4>Перевірка "Оцінка витрат"</h4>')

@login_required
def analytics(request):
    return HttpResponse('<h4>Перевірка "Аналітика перевиконання бюджету"</h4>')

@login_required
def readyMadeTemplates(request):
    return render(request, 'readyTemplates.html')

@login_required
def createBudget(request):
    # Отримуємо дані для відображення
    total_income = Budget.objects.aggregate(total=Sum('income'))['total'] or 0
    last_income_record = Budget.objects.order_by('-date', '-created_at').first()
    
    if request.method == 'POST':
        try:
            income = float(request.POST.get('income', 0))
            income_category = request.POST.get('income_category', 'salary')
            date = request.POST.get('date') or timezone.now().date()
            
            if income <= 0:
                messages.error(request, "Сума доходу має бути більше нуля")
                return render(request, 'createBudget.html', {
                    'total_income': total_income,
                    'last_income': last_income_record.income if last_income_record else 0,
                    'current_date': timezone.now().date()
                })
            
            # Створюємо новий запис
            Budget.objects.create(
                income=income,
                income_category=income_category,
                date=date,
                expenses=0,
                balance=income
            )
            
            messages.success(request, f"Дохід {income} грн успішно додано!")
            # Просте перенаправлення на ту саму сторінку
            return redirect('createBudget')  # Видалено reverse
            
        except ValueError:
            messages.error(request, "Будь ласка, введіть коректну суму доходу")
        except Exception as e:
            messages.error(request, f"Помилка при додаванні доходу: {str(e)}")
    
    return render(request, 'createBudget.html', {
        'total_income': total_income,
        'last_income': last_income_record.income if last_income_record else 0,
        'current_date': timezone.now().date()
    })
    
@login_required
def add_expense(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')

        if amount and category and date:
            expense = Expense.objects.create(
                amount=amount,
                category=category,
                date=date,
            )
            return JsonResponse({'status': 'success', 'message': 'Витрату додано!', 'expense_id': expense.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Будь ласка, заповніть всі поля.'})

    # GET-запит — просто показуємо список витрат
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'createPlan.html', {'expenses': expenses})

@login_required
def report_api(request):
    period = request.GET.get('period', 'month')
    date_str = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        date = datetime.now().date()
    
    # Отримуємо дані за вибраний період
    if period == 'day':
        # Дані за день
        expenses = Expense.objects.filter(date=date)
        budgets = Budget.objects.filter(created_at__date=date)
        
        labels = [f"{date.strftime('%d.%m.%Y')}"]
        xAxisTitle = "День"
        
    elif period == 'month':
        # Дані за місяць (по днях)
        start_date = date.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        expenses = Expense.objects.filter(date__range=[start_date, end_date])
        budgets = Budget.objects.filter(created_at__date__range=[start_date, end_date])
        
        # Генеруємо мітки для кожного дня місяця
        labels = []
        current_date = start_date
        while current_date <= end_date:
            labels.append(current_date.strftime('%d.%m'))
            current_date += timedelta(days=1)
        
        xAxisTitle = "Дні місяця"
        
    else:  # year
        # Дані за рік (по місяцях)
        start_date = date.replace(month=1, day=1)
        end_date = date.replace(month=12, day=31)
        
        expenses = Expense.objects.filter(date__range=[start_date, end_date])
        budgets = Budget.objects.filter(created_at__date__range=[start_date, end_date])
        
        labels = ['Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер', 'Лип', 'Сер', 'Вер', 'Жов', 'Лис', 'Гру']
        xAxisTitle = "Місяці року"
    
    # Підготовка даних для графіка
    if period == 'day':
        income = [float(budgets.aggregate(total=Sum('income'))['total'] or 0)]
        expenses_data = [float(expenses.aggregate(total=Sum('amount'))['total'] or 0)]
        
    elif period == 'month':
        income = [0] * end_date.day
        expenses_data = [0] * end_date.day
        
        # Розподіл доходів по днях
        for budget in budgets:
            day = budget.created_at.day - 1
            income[day] += float(budget.income)
        
        # Розподіл витрат по днях
        for expense in expenses:
            day = expense.date.day - 1
            expenses_data[day] += float(expense.amount)
            
    else:  # year
        income = [0] * 12
        expenses_data = [0] * 12
        
        # Розподіл доходів по місяцях
        for budget in budgets:
            month = budget.created_at.month - 1
            income[month] += float(budget.income)
        
        # Розподіл витрат по місяцях
        for expense in expenses:
            month = expense.date.month - 1
            expenses_data[month] += float(expense.amount)
    
    # Підготовка даних для таблиці
    transactions = []
    
    # Додаємо витрати
    for expense in expenses:
        transactions.append({
            'date': expense.date.strftime('%d.%m.%Y'),
            'type': 'Витрати',
            'amount': expense.amount,
            'category': expense.get_category_display()
        })
    
    # Додаємо доходи з їх датами
    for budget in budgets:
        transactions.append({
            'date': budget.created_at.strftime('%d.%m.%Y'),
            'type': 'Доходи',
            'amount': budget.income,
            'category': 'Зарплата'  # Можна додати поле категорії для доходів у моделі
        })
    
    # Сортуємо транзакції по даті
    transactions.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
    
    return JsonResponse({
        'labels': labels,
        'income': income,
        'expenses': expenses_data,
        'xAxisTitle': xAxisTitle,
        'transactions': transactions
    })

def logout_view(request):
    logout(request)  # Викликає функцію для виходу користувача
    return redirect('login')  # Перенаправлення на сторінку логіну

@login_required
def profile_view(request):
    """Відображення профілю користувача"""
    user = request.user
    context = {
        'user': user,
        'profile': user.profile
    }
    return render(request, 'profile.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Перенаправляємо на профіль після логіну
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        # Отримуємо поточного користувача
        user = request.user
        profile = user.profile

        # Оновлення повного імені
        if 'full_name' in request.POST:
            full_name = request.POST.get('full_name', '').strip()

            # Перевірка наявності пробілу для розділення на ім'я та прізвище
            if ' ' in full_name:
                first_name, last_name = full_name.split(' ', 1)
            else:
                first_name, last_name = full_name, ''
            
            # Оновлюємо ім'я та прізвище користувача
            user.first_name = first_name
            user.last_name = last_name
            user.save()  # Зберігаємо зміни користувача

            # Оновлюємо поле `full_name` в профілі
            profile.full_name = full_name
            profile.save()  # Зберігаємо зміни профілю

        # Оновлення інших даних профілю
        if 'gender' in request.POST:
            profile.gender = request.POST.get('gender', 'not_selected')

        if 'language' in request.POST:
            profile.language = request.POST.get('language', 'uk')

        # Зберігаємо зміни профілю
        profile.save()

        # Повертаємо повідомлення про успішне оновлення
        return JsonResponse({'status': 'success', 'message': 'Дані успішно збережено!'})

    # Якщо запит не POST, перенаправляємо на сторінку профілю
    return redirect('profile')



