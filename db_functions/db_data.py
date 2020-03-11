from accounts.models import TransactionId
from ture.models import Ture
from tbu.models import Tankning, Betaling, Udgift
from datetime import datetime
from accounts.models import Kirsten, Marie, Kasper, FarMor, OnBankAccount
#from kacaring import km_price


def _create_transaction(request, action_category):
    new_id = TransactionId(user=request.user, action=action_category)
    new_id.save()
    
    id_obj = TransactionId.objects.latest('transaction_id')
    return id_obj.transaction_id


def get_usernames(id_list):
    users = ['Kirsten','Marie','Kasper', 'Farmor & Farfar', 'Ukendt']
    active_users = eval(id_list)

    if isinstance(active_users, int):
        return users[active_users]
    else:
        user_names = [users[int(user)] for user in active_users]
        return user_names


def get_userID(user):
    if user == 'Kirsten':
        return 0
    elif user == 'Marie':
        return 1
    elif user == 'Kasper':
        return 2
    elif user == 'FarMor':
        return 3
    else:
        return None


def get_current_km():
    db_data = Ture.objects.latest('id')
    return db_data.km_count


def _get_latest_entry(user_id):
    if user_id == 0:
        db_data = Kirsten.objects.latest('id')
    elif user_id == 1:
        db_data = Marie.objects.latest('id')
    elif user_id == 2:
        db_data = Kasper.objects.latest('id')
    elif user_id == 3:
        db_data = FarMor.objects.latest('id')
    else:
        pass
    return db_data


def get_saldo(user_id):
    return _get_latest_entry(user_id).saldo


def get_bank_saldo():
    db_data = OnBankAccount.objects.latest('id')
    return db_data.saldo


def update_bank_account(transaction_id, amount, category, description):
    new_saldo = amount + get_bank_saldo()
    new_entry = OnBankAccount(saldo=new_saldo, category=category, description=description, timestamp=datetime.now(), transaction_id=transaction_id)
    new_entry.save()


def get_user_km(user_id):
    return _get_latest_entry(user_id).km


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


def get_user_data(user_id):
    user_data = []

    if user_id == 0:
        db_data = Kirsten.objects.all().order_by('-id')
        for entry in db_data:
            description = ''
            if entry.category == 'Udgift':
              udgift_data = get_db_entry(entry.transaction_id)
              description = udgift_data.description
            user_data.append({'date': entry.timestamp, 'saldo': entry.saldo, 'km': entry.km, 'category': entry.category, 'amount': entry.amount, 'description': description, 'transaction_id': entry.transaction_id })
        
    if user_id == 1:
        db_data = Marie.objects.all().order_by('-id')
        for entry in db_data:
            description = ''
            if entry.category == 'Udgift':
              udgift_data = get_db_entry(entry.transaction_id)
              description = udgift_data.description
            user_data.append({'date': entry.timestamp, 'saldo': entry.saldo, 'km': entry.km, 'category': entry.category, 'amount': entry.amount, 'description': description, 'transaction_id': entry.transaction_id })
        
    if user_id == 2:
        db_data = Kasper.objects.all().order_by('-id')
        for entry in db_data:
            description = ''
            if entry.category == 'Udgift':
              udgift_data = get_db_entry(entry.transaction_id)
              description = udgift_data.description
            user_data.append({'date': entry.timestamp, 'saldo': entry.saldo, 'km': entry.km, 'category': entry.category, 'amount': entry.amount, 'description': description, 'transaction_id': entry.transaction_id })
        
    if user_id == 3:
        db_data = FarMor.objects.all().order_by('-id')
        for entry in db_data:
            description = ''
            if entry.category == 'Udgift':
              udgift_data = get_db_entry(entry.transaction_id)
              description = udgift_data.description
            user_data.append({'date': entry.timestamp, 'saldo': entry.saldo, 'km': entry.km, 'category': entry.category, 'amount': entry.amount, 'description': description, 'transaction_id': entry.transaction_id })
        
    return user_data


def update_user_account(transaction_id, user_id, amount, km, category):
    print('----------- updated user account --------------')

    if user_id == 0:
        db_data = Kirsten.objects.latest('id')
        new_saldo = db_data.saldo + amount
        new_km = db_data.km + km
        new_entry = Kirsten(saldo=new_saldo, amount=amount, km=new_km, category=category, transaction_id=transaction_id)
        new_entry.save()
        print('----------- Kirsten --------------')
        
    elif user_id == 1:
        db_data = Marie.objects.latest('id')
        new_saldo = db_data.saldo + amount
        new_km = db_data.km + km
        new_entry = Marie(saldo=new_saldo, amount=amount, km=new_km, category=category, transaction_id=transaction_id)
        new_entry.save()
        print('----------- Marie --------------')

    elif user_id == 2:
        db_data = Kasper.objects.latest('id')
        new_saldo = db_data.saldo + amount
        new_km = db_data.km + km
        new_entry = Kasper(saldo=new_saldo, amount=amount, km=new_km, category=category, transaction_id=transaction_id)
        new_entry.save()
        print('----------- Kasper --------------')

    elif user_id == 3:
        db_data = FarMor.objects.latest('id')
        new_saldo = db_data.saldo + amount
        new_km = db_data.km + km
        new_entry = FarMor(saldo=new_saldo, amount=amount, km=new_km, category=category, transaction_id=transaction_id)
        new_entry.save()
        print('----------- Farmor & Farfar --------------')

    else:
        print('----------- error: user ID --------------')


def extra_pas(data):

    extra_pas = eval(data['extra_pas'])

    if extra_pas == 1:
        return [0, 1]
    if extra_pas == 2:
        return [1, 1]
    if extra_pas == 3:
        return [2, 1]
    if extra_pas == 4:
        return [3, 1]
    if extra_pas == 5:
        return [0, 2]
    if extra_pas == 6:
        return [1, 2]
    if extra_pas == 7:
        return [2, 2]
    if extra_pas == 8:
        return [3, 2]
    else:
        return [0, 0]


def update_accounts(request, form_data, category, km=0):
    new_id = _create_transaction(request, category)
    
    user_list = form_data['user_id']
    user_ids = eval(user_list)
    
    if isinstance(user_ids, int):
        if category == 'Tur':
            update_user_account(new_id, user_ids, form_data['amount'], km, category)
        elif category == 'Udgift': # deles altid mellem Kirsten, Marie og Kasper
            user_amount = form_data['amount'] / 3
            update_user_account(new_id, 0, user_amount, km, category)
            update_user_account(new_id, 1, user_amount, km, category)
            update_user_account(new_id, 2, user_amount, km, category)

            update_user_account(new_id, user_ids, -form_data['amount'], km, category)
        else:
            update_user_account(new_id, user_ids, -form_data['amount'], km, category)
    
    else:
        number_of_users = len(user_ids)
        if category == 'Tur':
            number_of_users + extra_pas(form_data)[1]

        for user in user_ids:
            user = int(user)
            user_amount = form_data['amount'] / number_of_users
            
            if category == 'Tur':        
                update_user_account(new_id, user, user_amount, km, category)
            else:
                update_user_account(new_id, user, -user_amount, km, category)

        if category == 'Tur' and extra_pas(form_data)[1]:
            user = extra_pas(form_data)[0]
            user_amount = user_amount + user_amount * extra_pas(form_data)[1]
            _update_saldo(new_id, extra_pas(form_data)[0], user_amount)

    return new_id


def delete_transaction(request, transaction_id):
    instance = TransactionId.objects.get(transaction_id=transaction_id)
    orig_timestamp = instance.timestamp
    instance.delete()

    reenter_transaction = TransactionId(transaction_id=transaction_id, timestamp=orig_timestamp, action=instance.action)
    reenter_transaction.save()

    category = str(instance.action) + ' deleted'
    print(category)
    _create_transaction(request, category)


def update_user_saldo(transaction_id, user_id, amount):
    
    user_ids = eval(user_id)
    
    if isinstance(user_ids, int):
        _update_saldo(transaction_id, user_ids, amount)
    else:
        number_of_users = len(user_ids)
        for user in user_ids:
            user_id = int(user)
            user_amount = amount / number_of_users
            _update_saldo(transaction_id, user_id, user_amount)


def _update_saldo(transaction_id, user_id, amount):
    if user_id == 0:
        user_data = Kirsten.objects.get(transaction_id=transaction_id)
        user_data.amount = amount
        user_data.save()
        _recalc_user_saldo(user_id)
    
    elif user_id == 1:
        user_data = Marie.objects.get(transaction_id=transaction_id)
        user_data.amount = amount
        user_data.save()
        _recalc_user_saldo(user_id)
    
    elif user_id == 2:
        user_data = Kasper.objects.get(transaction_id=transaction_id)
        user_data.amount = amount
        user_data.save()
        _recalc_user_saldo(user_id)
    
    elif user_id == 3:
        user_data = FarMor.objects.get(transaction_id=transaction_id)
        user_data.amount = amount
        user_data.save()
        _recalc_user_saldo(user_id)
    else:
        pass


def _update_km(transaction_id, user_id, delta_km):
    if user_id == 0:
        user_data = Kirsten.objects.get(transaction_id=transaction_id)
        try:
            prior_entry = Kirsten.objects.get(id=user_data.id - 1)
            last_km = prior_entry.km_count
            user_data.km_count = last_km + delta_km
            user_data.save()
            _recalc_user_saldo(user_id)
        except:
            pass
        
    elif user_id == 1:
        user_data = Marie.objects.get(transaction_id=transaction_id)
        try:
            prior_entry = Marie.objects.get(id=user_data.id - 1)
            last_km = prior_entry.km_count
            user_data.km_count = last_km + delta_km
            user_data.save()
            _recalc_user_saldo(user_id)
        except:
            pass
    
    elif user_id == 2:
        user_data = Kasper.objects.get(transaction_id=transaction_id)
        try:
            prior_entry = Kasper.objects.get(id=user_data.id - 1)
            last_km = prior_entry.km_count
            user_data.km_count = last_km + delta_km
            user_data.save()
            _recalc_user_saldo(user_id)
        except:
            pass
    
    elif user_id == 3:
        user_data = FarMor.objects.get(transaction_id=transaction_id)
        try:
            prior_entry = FarMor.objects.get(id=user_data.id - 1)
            last_km = prior_entry.km_count
            user_data.km_count = last_km + delta_km
            user_data.save()
            _recalc_user_saldo(user_id)
        except:
            pass
    else:
        pass


def _recalc_user_saldo(user_id):
    saldo = 0.0

    if user_id == 0:
        user_data = Kirsten.objects.all().order_by('id')
        for entry in user_data:
            orig_timestamp = entry.timestamp
            saldo += entry.amount
            entry.saldo = saldo
            entry.timestamp = orig_timestamp
        
            entry.save()
    
    elif user_id == 1:
        user_data = Marie.objects.all().order_by('id')
        for entry in user_data:
            orig_timestamp = entry.timestamp
            saldo += entry.amount
            entry.saldo = saldo
            entry.timestamp = orig_timestamp
        
            entry.save()
    
    elif user_id == 2:
        user_data = Kasper.objects.all().order_by('id')
        for entry in user_data:
            orig_timestamp = entry.timestamp
            saldo += entry.amount
            entry.saldo = saldo
            entry.timestamp = orig_timestamp
        
            entry.save()
    
    elif user_id == 3:
        user_data = FarMor.objects.all().order_by('id')
        for entry in user_data:
            orig_timestamp = entry.timestamp
            saldo += entry.amount
            entry.saldo = saldo
            entry.timestamp = orig_timestamp
        
            entry.save()
    else:
        pass


def update_user_km(transaction_id, user_id, delta_km, price):
    user_ids = eval(user_id)
    
    if isinstance(user_ids, int):
        amount = price
        _update_saldo(transaction_id, user_ids, amount)
        _update_km(transaction_id, user_ids, delta_km)
    else:
        number_of_users = len(user_ids)
        for user in user_ids:
            user_id = int(user)
            user_amount = price / number_of_users
            _update_saldo(transaction_id, user_id, user_amount)
            _update_km(transaction_id, user_id, delta_km)

