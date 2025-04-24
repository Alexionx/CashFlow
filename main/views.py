from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import BudgetForm
from .models import Budget, Expense
from django.contrib.auth.decorators import login_required

# Функція для реєстрації
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Отримуємо дані форми
            user = form.save(commit=False)  # Не зберігаємо ще користувача
            user.set_password(form.cleaned_data['password'])  # Хешуємо пароль
            user.save()  # Зберігаємо користувача з хешованим паролем
            login(request, user)  # Авторизуємо користувача після реєстрації
            return redirect('home')  # Перенаправлення на сторінку профілю
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
def createBudget(request):
    return render(request, 'createBudget.html')

@login_required
def readyMadeTemplates(request):
    return render(request, 'readyTemplates.html')

@login_required
def createBudget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createBudget')  # Перенаправлення після збереження
    else:
        form = BudgetForm()

    # Отримуємо останній бюджет (можна змінити логіку)
    last_budget = Budget.objects.last()
    income = last_budget.income if last_budget else 0
    expenses = 50000  # Ти можеш зробити модель "витрати"
    balance = income - expenses

    return render(request, 'createBudget.html', {
        'form': form,
        'income': income,
        'expenses': expenses,
        'balance': balance
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        # Отримуємо дані з форми
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')

        if amount and category and date:
            # Створюємо новий запис у базі даних
            expense = Expense.objects.create(
                amount=amount,
                category=category,
                date=date,
            )
            return JsonResponse({'status': 'success', 'message': 'Витрату додано!', 'expense_id': expense.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Будь ласка, заповніть всі поля.'})
    return render(request, 'createPlan.html')

def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()  # Зберігаємо новий бюджет
    else:
        form = BudgetForm()

    # Отримуємо останній бюджет
    try:
        budget = Budget.objects.latest('id')  # Отримуємо останній запис бюджету
        income = budget.income
        expenses = budget.expenses
        balance = budget.balance
    except Budget.DoesNotExist:
        income = expenses = balance = 0

    return render(request, 'create_budget.html', {
        'form': form,
        'income': income,
        'expenses': expenses,
        'balance': balance,
    })