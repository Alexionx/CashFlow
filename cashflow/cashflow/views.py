from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def home(request):
    return HttpResponse('Hello, World!')


def home(request):
    return render(request, 'home.html')  # Повертаємо шаблон

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматичний вхід після реєстрації
            return redirect("home")  # Переадресація на головну
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})