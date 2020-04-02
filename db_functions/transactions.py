from accounts.models import TransactionId
from ture.models import Ture
from tbu.models import Tankning, Betaling, Udgift
from datetime import datetime
from accounts.models import Kirsten, Marie, Kasper, FarMor, OnBankAccount
from emailing.models import UserPreferences, EmailQue
from django.contrib.auth.models import User
from django.apps import apps
import accounts


def create_new_transaction(request, action_category):
    new_id = TransactionId(user=request.user, action=action_category)
    new_id.save()
    
    id_obj = TransactionId.objects.latest('transaction_id')
    return id_obj.transaction_id


def get_db_entry(search_key):
    try:
        db_entry = Ture.objects.get(transaction_id=search_key)
        return db_entry
    except Ture.DoesNotExist:
        pass
    try:
        db_entry = Tankning.objects.get(transaction_id=search_key)
        return db_entry
    except Tankning.DoesNotExist:
        pass
    try:
        db_entry = Betaling.objects.get(transaction_id=search_key)
        return db_entry
    except Betaling.DoesNotExist:
        pass
    try:
        db_entry = Udgift.objects.get(transaction_id=search_key)
        return db_entry
    except Udgift.DoesNotExist:
        return None



###############################
#        Totals data          #
###############################

def get_current_km():
    db_data = Ture.objects.latest('id')
    return db_data.km_count


def get_total_tankning():
    db_data = Tankning.objects.all()
    for entry in db_data:
      total =+ entry.amount
    return total



###############################
#         Bank account        #
###############################

def get_bank_saldo():
    db_data = OnBankAccount.objects.latest('id')
    return db_data.saldo


def update_bank_account(transaction_id, amount, user_id, category, description=''):
    new_saldo = amount + get_bank_saldo()
    new_entry = OnBankAccount(saldo=new_saldo, category=category, user=user_id, timestamp=datetime.now(), description=description, transaction_id=transaction_id)
    new_entry.save()




###############################
#     data for viewing        #
###############################


def get_all_data():
    all_data = []

    ture = Ture.objects.all().order_by('-id')
    for tur in ture:
        all_data.append({'date': tur.date, 'km_count': tur.km_count, 'users': get_usernames(tur.user_id), 'extra_pas': extra_pas({'extra_pas': tur.extra_pas}), 'type': 'Kørsel', 'km': tur.delta_km, 'amount': tur.price, 'table_id': tur.id, 'transaction_id': tur.transaction_id})
    
    tankninger = Tankning.objects.all().order_by('-id')
    for tankning in tankninger:
        all_data.append({'date': tankning.date, 'amount': -tankning.amount, 'users': [get_usernames(tankning.user_id)], 'type': 'Tankning', 'table_id': tankning.id, 'transaction_id': tankning.transaction_id})
    
    betalinger = Betaling.objects.all().order_by('-id')
    for betaling in betalinger:
        if betaling.amount > 0:
          all_data.append({'date': betaling.date, 'amount': betaling.amount, 'users': [get_usernames(betaling.user_id)], 'type': 'Indbetaling', 'table_id': betaling.id, 'transaction_id': betaling.transaction_id})
        else:
          all_data.append({'date': betaling.date, 'amount': -betaling.amount, 'users': [get_usernames(betaling.user_id)], 'type': 'Udbetaling', 'table_id': betaling.id, 'transaction_id': betaling.transaction_id})

    udgifter = Udgift.objects.all().order_by('-id')
    for udgift in udgifter:
        all_data.append({'date': udgift.date, 'amount': udgift.amount, 'description': udgift.description, 'users': [get_usernames(udgift.user_id)], 'type': 'Udgift', 'table_id': udgift.id, 'transaction_id': udgift.transaction_id})
    
    all_data_sorted = sorted(all_data, key=lambda k: k['date'], reverse=True)
    return all_data_sorted