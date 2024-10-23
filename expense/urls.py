from django.urls import path
from .views import addExpense, listExpenses, getOverallExpenses, balanceSheet

urlpatterns = [
    path('add/', addExpense, name='add-expense'),  # URL to add an expense
    path('list/', listExpenses, name='list-expenses'),  # URL to list individual user expenses
    path('overall/', getOverallExpenses, name='overall-expenses'),  # URL to retrieve overall expenses
    path('download/balance-sheet/', balanceSheet, name='balance-sheet'),  # URL to download balance sheet
]
