from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def register(request):
    return render(request, 'registration.html')

def profile(request):
    return render(request, 'profile.html')

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