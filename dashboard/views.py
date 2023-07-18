from django.shortcuts import render
from . import logics 

def home(request):
    balance = logics.account_balance_for_view()
    checks = logics.checks_for_view()
    sales = logics.sold_for_view()
    content = {
        'balance': balance[0],
        'total': balance[1],
        'checks':checks,
        'sales':sales
    }
    return render(request, 'dashboard/home.html', content)
