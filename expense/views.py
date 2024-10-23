from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Expense, Participant
from user.models import User
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.urls import reverse
import csv
import requests

BASE_URL = 'http://localhost:8000'

@csrf_exempt
def addExpense(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            description = data.get('description')
            amount = data.get('amount')
            date = data.get('date')
            payerId = data.get('payer_id')
            paymentType = data.get('payment_type')
            participantsData = data.get('participants')

            if not all([description, amount, date, payerId, paymentType, participantsData]):
                return JsonResponse({'error': 'All fields are required'}, status=400)

            try:
                payer = get_object_or_404(User, id=int(payerId))
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Payer does not exist'}, status=404)

            totalAmount = float(amount)
            exactSum = 0
            percentageSum = 0

            for participantData in participantsData:
                if paymentType == "exact":
                    exactSum += float(participantData['amount'])
                elif paymentType == "percentage":
                    percentageSum += float(participantData['amount'])

            if paymentType == "exact" and exactSum != totalAmount:  # Check whether individual sums amount to total sum
                return JsonResponse({'error': 'Exact amounts do not sum up to the total expense amount'}, status=400)
            elif paymentType == "percentage" and percentageSum != 100:  # Check whether all percentages sum to 100
                return JsonResponse({'error': 'Percentages do not sum up to 100%'}, status=400)

            with transaction.atomic():
                expense = Expense.objects.create(
                    description=description,
                    amount=totalAmount,
                    date=date,
                    payer=payer,
                    payment_type=paymentType
                )

                for participantData in participantsData:
                    user = User.objects.get(id=participantData['user_id'])
                    if paymentType == "percentage":
                        participantAmount = (float(participantData['amount']) / 100) * totalAmount
                    else:
                        participantAmount = float(participantData['amount'])

                    Participant.objects.create(expense=expense, user=user, amount=participantAmount)

            return JsonResponse({'message': 'Expense created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def listExpenses(request, userId):
    try:
        user = get_object_or_404(User, id=userId)

        participantEntries = Participant.objects.filter(user=user).exclude(expense__payer=user)
        payerEntries = Expense.objects.filter(payer=user)

        userExpenses = []

        totalOwed = 0
        totalPaid = 0

        for entry in participantEntries:
            expense = entry.expense
            totalOwed += entry.amount  # Money is owed if user is a participant in an expense
            userExpenses.append({
                'expenseId': expense.id,
                'description': expense.description,
                'amount': expense.amount,
                'date': expense.date,
                'payer': expense.payer.name,
                'paymentType': expense.payment_type,
                'amountOwed': entry.amount
            })

        for expense in payerEntries:
            totalPaid += expense.amount  # Money is paid if user is the payer of expense
            userExpenses.append({
                'expenseId': expense.id,
                'description': expense.description,
                'amount': expense.amount,
                'date': expense.date,
                'payer': user.name,
                'paymentType': expense.payment_type,
                'amountPaid': expense.amount
            })

        netOwed = totalPaid - totalOwed

        return JsonResponse({
            'expenses': userExpenses,
            'totalOwed': totalOwed,
            'totalPaid': totalPaid,
            'netOwed': netOwed
        }, status=200, safe=False)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def getOverallExpenses(request):
    try:
        expenses = Expense.objects.all()

        overallExpenses = []

        for expense in expenses:
            participants = Participant.objects.filter(expense=expense)
            participantDetails = []

            for participant in participants:  # Find details of all participants in an expense
                participantDetails.append({
                    'userId': participant.user.id,
                    'username': participant.user.name,
                    'amount': participant.amount
                })

            overallExpenses.append({  # Add expense details as well as participant details
                'expenseId': expense.id,
                'description': expense.description,
                'amount': expense.amount,
                'date': expense.date,
                'payer': expense.payer.name,
                'paymentType': expense.payment_type,
                'participants': participantDetails
            })

        return JsonResponse({
            'overallExpenses': overallExpenses,
        }, status=200, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def balanceSheet(request, userId=None):
    if request.method == 'GET':
        try:
            if userId:
                individualExpensesUrl = reverse('get_individual_expenses', args=[userId])
                individualExpensesResponse = requests.get(f"{BASE_URL}{individualExpensesUrl}")  # Call Individual Expense
                individualExpensesResponse.raise_for_status()
                individualExpenses = individualExpensesResponse.json()
            else:
                individualExpenses = {'expenses': []}

            overallExpensesUrl = reverse('get_overall_expenses')
            overallExpensesResponse = requests.get(f"{BASE_URL}{overallExpensesUrl}")  # Call Overall Expense
            overallExpensesResponse.raise_for_status()
            overallExpenses = overallExpensesResponse.json()

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

            writer = csv.writer(response)
            # Headings of CSV File
            writer.writerow([
                'Type', 'Expense ID', 'Description', 'Amount', 'Date',
                'Payer Name', 'Payment Type', 'Amount Owed', 'Amount Paid'
            ])

            if userId:
                # Individual expenses
                for expense in individualExpenses['expenses']:
                    amountOwed = expense.get('amountOwed', 0)
                    amountPaid = expense.get('amountPaid', 0)
                    writer.writerow([
                        'Individual',
                        expense['expenseId'],
                        expense['description'],
                        expense['amount'],
                        expense['date'],
                        expense['payer'],
                        expense['paymentType'],
                        amountOwed,
                        amountPaid
                    ])
                # Overall Expenses
                writer.writerow([
                    'Type', 'Expense ID', 'Description', 'Amount', 'Date',
                    'Payer Name', 'Payment Type', 'ParticipantId', 'ParticipantName', 'Amount'
                ])
                for expense in overallExpenses['overallExpenses']:
                    for participant in expense['participants']:
                        writer.writerow([
                            'Overall',
                            expense['expenseId'],
                            expense['description'],
                            expense['amount'],
                            expense['date'],
                            expense['payer'],
                            expense['paymentType'],
                            participant['userId'],
                            participant['username'],
                            participant['amount']
                        ])

            return response

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Error fetching data: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
