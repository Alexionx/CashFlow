from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('createPlan/', views.createPlan, name='createPlan'),
    path('currentBudget/', views.currentBudget, name='currentBudget'),
    path('costs/', views.costs, name='costs'),
    path('chart/', views.chart, name='chart'),
    path('analytics/', views.analytics, name='analytics'),
    path('budgetBalanceEstimate/', views.budgetBalanceEstimate, name='budgetBalanceEstimate'),
    path('readyMadeTemplates/', views.readyMadeTemplates, name='readyMadeTemplates'),
]