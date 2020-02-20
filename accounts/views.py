from django.shortcuts import render
from db_functions.db_data import get_saldo, get_user_km, get_all_data, get_db_entry, update_user_saldo, get_usernames, get_userID, delete_transaction, recalc_ture
from django.views.generic import DeleteView
from .models import TransactionId


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


def show_user_transactions(request, userIDname):
    all_data = get_all_data()
    all_user_data = []

    userID = get_userID(userIDname)

    for user_data in all_data:
        for user_name in user_data['users']:
            if user_name == userIDname:
                print(user_data)
                user_data['amount'] = user_data['amount'] / len(user_data['users'])
                all_user_data.append(user_data)

    context = {'user': userIDname, 'user_km': get_user_km(userID), 'entries': all_user_data, 'user_saldo': get_saldo(userID) }
    return render(request, 'user_transactions.html', context)


def delete_entry(request, entry_id):
    delete_transaction(request, entry_id)
    return render(request, 'index.html')


class TransactionDelete(DeleteView):
    model = TransactionId
    template_name = 'transactionid_confirm_delete.html'
    success_url = '/'


# def edit_entry(request, transaction_id):
#     db_entry = get_db_entry(transaction_id)
#     print(db_entry.price)
#     context = {'date': db_entry.date, 'amount': db_entry.price, 'transaction_id': transaction_id}
#     return render(request, 'edit_entries.html', context)

