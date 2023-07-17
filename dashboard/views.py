from django.shortcuts import render
from . import logics 

def home(request):
    content = {
        'balance': 100
    }
    return render(request, 'dashboard/home.html', content)
