from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import BudgetForm
from .models import Budget

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
def profile(request):
    return render(request, 'profile.html')

# Інші функції
def createPlan(request):
    return render(request, 'createPlan.html')

def chart(request):
    return render(request, 'chart.html')

def costs(request):
    return HttpResponse('<h4>Перевірка "Оцінка витрат"</h4>')

def analytics(request):
    return HttpResponse('<h4>Перевірка "Аналітика перевиконання бюджету"</h4>')

def createBudget(request):
    return render(request, 'createBudget.html')

def readyMadeTemplates(request):
    return render(request, 'readyTemplates.html')

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