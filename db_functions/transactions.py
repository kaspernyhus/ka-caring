from accounts.models import TransactionId
from ture.models import Ture
from tbu.models import Tankning, Betaling, Udgift
from accounts.models import *
from datetime import datetime
from django.apps import apps
from db_functions.users import get_usernames, get_firstnames, extra_pas


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


def get_total_km():
  km = get_current_km()
  km = km - 114293 #km ved overtagelse
  return km


def get_total_tankning():
    db_data = Tankning.objects.all()
    for entry in db_data:
      total =+ entry.amount
    return total


def get_total_udgift():
    db_data = Udgift.objects.all()
    for entry in db_data:
      total =+ entry.amount
    return total


###############################
#        User accounts        #
###############################

def update_accounts(request, new_id, form_data, category, km=0):
    user_list = form_data['user_id']
    user_id = eval(user_list)

    ### ROUTER ###

    if category == 'Indskud':
        update_bank_account(new_id, user_id, form_data['amount'], category)
        update_user_account(new_id, user_id, 0, category)

    elif category == 'Indbetaling':
        update_bank_account(new_id, user_id, form_data['amount'], category)
        update_user_account(new_id, user_id, -form_data['amount'], category)

    elif category == 'Udbetaling':
        update_bank_account(new_id, user_id, -form_data['amount'], category)
        update_user_account(new_id, user_id, form_data['amount'], category)

    elif category == 'Tankning':
        update_user_account(new_id, user_id, -form_data['amount'], category)

    elif category == 'Udgift':
        if form_data['user_id'] == '0': # Fælles-konto'en
            update_bank_account(new_id, user_id, -form_data['amount'], category)
        else:
            update_user_account(new_id, user_id, -form_data['amount'], category)

    elif category == 'Tur':
        if user_id == ['100']: #Tur mangler!
            print('----------- Tur mangler ! ------------')
            pass
        else:
            number_of_users = len(user_id)
            number_of_users + extra_pas(form_data)[1]
            user_amount = form_data['amount'] / number_of_users

            for user in user_id:
                userid = eval(user)
                update_user_account(new_id, userid, user_amount, category, km=km)

            if extra_pas(form_data)[1]:
                user = extra_pas(form_data)[0]
                user_amount = user_amount + user_amount * extra_pas(form_data)[1]
                _update_user_saldo(new_id, extra_pas(form_data)[0], user_amount)


def update_user_account(transaction_id, user_id, amount, category, km=0):
    username = get_usernames(user_id)
    Model = apps.get_model('accounts', username)

    db_data = Model.objects.latest('id')
    new_saldo = db_data.saldo + amount
    new_km = db_data.km + km
    new_entry = Model(saldo=new_saldo, amount=amount, km=new_km, category=category, transaction_id=transaction_id)
    new_entry.save()
    

def update_user_saldo(transaction_id, user_id, amount):
    user_ids = eval(user_id)
    
    if isinstance(user_ids, int):
        _update_user_saldo(transaction_id, user_ids, amount)
    else:
        number_of_users = len(user_ids)
        for user in user_ids:
            user_id = int(user)
            user_amount = amount / number_of_users
            _update_user_saldo(transaction_id, user_id, user_amount)


def _update_user_saldo(transaction_id, user_id, amount):
    username = get_user_info('get_user_names', user_id)
    Model = apps.get_model('accounts', username)
    
    user_data = Model.objects.get(transaction_id=transaction_id)
    user_data.amount = amount
    user_data.save()
    _recalc_user_saldo(user_id)


def update_user_km(transaction_id, user_id, delta_km, price):
    user_ids = eval(user_id)
    
    if isinstance(user_ids, int):
        amount = price
        _update_user_saldo(transaction_id, user_ids, amount)
        _update_user_km(transaction_id, user_ids, delta_km)
    else:
        number_of_users = len(user_ids)
        for user in user_ids:
            user_id = int(user)
            user_amount = price / number_of_users
            _update_user_saldo(transaction_id, user_id, user_amount)
            _update_user_km(transaction_id, user_id, delta_km)


def _update_user_km(transaction_id, user_id, delta_km):
    username = get_usernames(user_id)
    Model = apps.get_model('accounts', username)
    
    user_data = Model.objects.get(transaction_id=transaction_id)
    try:
        prior_entry = Model.objects.get(id=user_data.id - 1)
        last_km = prior_entry.km_count
        user_data.km_count = last_km + delta_km
        user_data.save()
        _recalc_user_saldo(user_id)
    except:
        pass


def _recalc_user_saldo(user_id):
    saldo = 0.0
    
    username = get_usernames(user_id)
    Model = apps.get_model('accounts', username)
    
    user_data = Model.objects.all().order_by('id')
    for entry in user_data:
      orig_timestamp = entry.timestamp
      saldo += entry.amount
      entry.saldo = saldo
      entry.timestamp = orig_timestamp
      entry.save()



###############################
#         Bank account        #
###############################

def get_bank_saldo():
    db_data = OnBankAccount.objects.latest('id')
    return db_data.saldo


def update_bank_account(transaction_id, user_id, amount, category, description=''):
    new_saldo = amount + get_bank_saldo()
    new_entry = OnBankAccount(saldo=new_saldo, category=category, user=user_id, timestamp=datetime.now(), description=description, transaction_id=transaction_id)
    new_entry.save()


def get_bank_transactions():
    bank_account = OnBankAccount.objects.all().order_by('-id')

    account_data = []

    for transaction in bank_account:
        try:
            amount = get_db_entry(transaction.transaction_id).amount
        except:
            pass
        account_data.append({'date': transaction.timestamp, 'category': transaction.category, 'user': get_firstnames(transaction.user), 'amount': amount, 'saldo': transaction.saldo, 'description': transaction.description})

    return account_data




###############################
#     data for viewing        #
###############################

def get_all_data():
    all_data = []

    ture = Ture.objects.all().order_by('-id')
    for tur in ture:
        all_data.append({'date': tur.date, 'km_count': tur.km_count, 'users': get_firstnames(eval(tur.user_id)), 'extra_pas': extra_pas({'extra_pas': tur.extra_pas}), 'type': 'Kørsel', 'km': tur.delta_km, 'amount': tur.price, 'table_id': tur.id, 'transaction_id': tur.transaction_id})
    
    tankninger = Tankning.objects.all().order_by('-id')
    for tankning in tankninger:
        all_data.append({'date': tankning.date, 'amount': -tankning.amount, 'users': [get_firstnames(eval(tankning.user_id))], 'type': 'Tankning', 'table_id': tankning.id, 'transaction_id': tankning.transaction_id})
    
    betalinger = Betaling.objects.all().order_by('-id')
    for betaling in betalinger:
        if betaling.amount < 0:
          all_data.append({'date': betaling.date, 'amount': -betaling.amount, 'users': [get_firstnames(betaling.user_id)], 'type': 'Udbetaling', 'table_id': betaling.id, 'transaction_id': betaling.transaction_id})
        elif betaling.is_indskud:
            all_data.append({'date': betaling.date, 'amount': betaling.amount, 'users': [get_firstnames(betaling.user_id)], 'type': 'Indskud', 'table_id': betaling.id, 'transaction_id': betaling.transaction_id})
        else:
            all_data.append({'date': betaling.date, 'amount': betaling.amount, 'users': [get_firstnames(betaling.user_id)], 'type': 'Indbetaling', 'table_id': betaling.id, 'transaction_id': betaling.transaction_id})

    udgifter = Udgift.objects.all().order_by('-id')
    for udgift in udgifter:
        all_data.append({'date': udgift.date, 'amount': -udgift.amount, 'description': udgift.description, 'users': [get_firstnames(udgift.user_id)], 'type': 'Udgift', 'table_id': udgift.id, 'transaction_id': udgift.transaction_id})
    
    all_data_sorted = sorted(all_data, key=lambda k: k['date'], reverse=True)
    return all_data_sorted