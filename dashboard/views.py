from django.shortcuts import render
from . import logics 

def home(request):
    balance = logics.account_balance_for_view()
    content = {
        'balance': balance[1]
    }
    return render(request, 'dashboard/home.html', content)
