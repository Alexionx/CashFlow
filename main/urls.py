from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('createPlan/', views.createPlan, name='createPlan'),
    path('createBudget/', views.createBudget, name='createBudget'),
    path('chart/', views.chart, name='chart'),
    path('analytics/', views.analytics, name='analytics'),
    path('readyMadeTemplates/', views.readyMadeTemplates, name='readyMadeTemplates'),
]