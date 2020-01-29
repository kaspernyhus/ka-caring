from django.shortcuts import render
from db_functions.db_data import get_saldo, get_user_km


def oversigt(request):
    context = {
        'kirsten_saldo': get_saldo(0), 
        'marie_saldo': get_saldo(1), 
        'kasper_saldo': get_saldo(2), 
        'kirsten_km': get_user_km(0), 
        'marie_km': get_user_km(1),
        'kasper_km': get_user_km(2),
        'total_km': 100
        }

    return render(request, 'oversigt.html', context)



