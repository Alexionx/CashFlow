from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

# Функція для реєстрації
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Зберігає користувача в базу даних
            login(request, user)  # Авторизує користувача після реєстрації
            return redirect('home')  # Перенаправлення на сторінку профілю
    else:
        form = UserRegistrationForm()

    return render(request, 'registration.html', {'form': form})

# Функція для входу
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправлення на сторінку профілю після входу
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Функція для профілю
def profile(request):
    return render(request, 'profile.html')

# Інші функції
def createPlan(request):
    return HttpResponse('<h4>Перевірка "Створення плану"</h4>')

def currentBudget(request):
    return HttpResponse('<h4>Перевірка "Поточний бюджет"</h4>')

def costs(request):
    return HttpResponse('<h4>Перевірка "Оцінка витрат"</h4>')

def chart(request):
    return HttpResponse('<h4>Перевірка "Кругова діаграма"</h4>')

def analytics(request):
    return HttpResponse('<h4>Перевірка "Аналітика перевиконання бюджету"</h4>')

def budgetBalanceEstimate(request):
    return HttpResponse('<h4>Перевірка "Оцінка залишку бюджету на кінець місяця"</h4>')

def readyMadeTemplates(request):
    return HttpResponse('<h4>Перевірка "Готові шаблони"</h4>')
