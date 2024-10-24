from django.urls import path
from .views import addExpense, listExpenses, getOverallExpenses, balanceSheet

urlpatterns = [
    path('add/', addExpense, name='addExpense'),  # URL to add an expense
    path('list/<int:userId>', listExpenses, name='listExpenses'),  # URL to list individual user expenses
    path('overall/', getOverallExpenses, name='getOverallExpenses'),  # URL to retrieve overall expenses
    path('download/balance-sheet/<int:userId>', balanceSheet, name='balanceSheet'),  # URL to download balance sheet
]
