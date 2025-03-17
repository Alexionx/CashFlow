from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def register(request):
    return render(request, 'registration.html')

def profile(request):
    return render(request, 'profile.html')

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