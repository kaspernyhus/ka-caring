from django.shortcuts import render
from db_functions.db_data import get_saldo, get_user_km, get_all_data


def oversigt(request):
    context = {
        'kirsten_saldo': get_saldo(0), 
        'marie_saldo': get_saldo(1), 
        'kasper_saldo': get_saldo(2),
        'farmor_saldo': get_saldo(3), 
        'kirsten_km': get_user_km(0), 
        'marie_km': get_user_km(1),
        'kasper_km': get_user_km(2),
        'farmor_km': get_user_km(3),
        'total_km': 100
        }
    return render(request, 'oversigt.html', context)


def show_all_transactions(request):
    all_data = get_all_data()
    context = {'entries': all_data}

    return render(request, 'all_transactions.html', context)


def show_user_transactions(request):
    all_data = get_all_data()
    all_user_data = [user_data for user_data in all_data if user_data['users'] == ['Kasper']]
    context = {'user': 'Kasper', 'user_km': get_user_km(2), 'entries': all_user_data}

    return render(request, 'user_transactions.html', context)


def edit_entry(request, transaction_id):
    context = {'transaction_id': transaction_id}
    return render(request, 'edit_entries.html', context)