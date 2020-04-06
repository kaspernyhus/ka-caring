from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from db_functions.users import get_user_saldo, get_user_km, get_user_data, is_VIP
from db_functions.transactions import get_all_data, get_bank_saldo, get_bank_transactions
from django.views.generic import DeleteView
from .models import TransactionId
from kacaring.km_price import get_km_price


@login_required(login_url='login')
@user_passes_test(is_VIP, login_url='guest_oversigt')
def oversigt(request):
    context = {
        'kirsten_saldo': get_user_saldo(8), 
        'marie_saldo': get_user_saldo(9), 
        'kasper_saldo': get_user_saldo(7),
        'farmor_saldo': get_user_saldo(10), 
        'kirsten_km': get_user_km(8), 
        'marie_km': get_user_km(9),
        'kasper_km': get_user_km(7),
        'farmor_km': get_user_km(10),
        'km_price': get_km_price(request.user.groups),
        'bank_saldo': get_bank_saldo(),
        }
    return render(request, 'oversigter/oversigt.html', context)


def guest_oversigt(request):
    context = {
        'username': request.user.username,
        'user_saldo': get_user_saldo(request.user.id),
        'user_km': get_user_km(request.user.id)
        }
    return render(request, 'oversigter/guest_oversigt.html', context)


@login_required(login_url='login')
def show_all_transactions(request):
    context = {'entries': get_all_data()[:-1]}
    return render(request, 'oversigter/all_transactions.html', context)


@login_required(login_url='login')
def show_user_transactions(request, username):
    user_data = get_user_data(username)
    context = {'user': username, 'entries': user_data[:-1]}
    return render(request, 'oversigter/user_transactions.html', context)


@login_required(login_url='login')
def show_bank_transactions(request):
    account_data = get_bank_transactions()
    context = {'entries': account_data[:-1]}
    return render(request, 'oversigter/bank_account_transactions.html', context)


class TransactionDelete(DeleteView):
    model = TransactionId
    template_name = 'transactions/transactionid_confirm_delete.html'
    success_url = '/oversigt/alle_transaktioner'

