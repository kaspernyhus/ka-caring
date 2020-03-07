from django.shortcuts import render
from db_functions.db_data import get_saldo, get_user_km, get_all_data, get_user_data, get_db_entry, update_user_saldo, get_usernames, get_userID, delete_transaction
from django.views.generic import DeleteView
from .models import TransactionId
from kacaring.km_price import get_km_price


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
        'km_price': get_km_price()
        }
    return render(request, 'oversigt.html', context)


def show_all_transactions(request):
    all_data = get_all_data()
    print(all_data)
    context = {'entries': all_data}
    return render(request, 'all_transactions.html', context)


def show_user_transactions(request, userIDname):
    userID = get_userID(userIDname)

    user_data = get_user_data(userID)
    
    context = {'user': userIDname, 'entries': user_data}
    return render(request, 'user_transactions.html', context)


def delete_entry(request, entry_id):
    delete_transaction(request, entry_id)
    return render(request, 'index.html')


class TransactionDelete(DeleteView):
    model = TransactionId
    template_name = 'transactionid_confirm_delete.html'
    success_url = '/oversigt/alle_transaktioner'

