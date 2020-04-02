from accounts.models import TransactionId
from ture.models import Ture
from tbu.models import Tankning, Betaling, Udgift
from datetime import datetime
from accounts.models import Kirsten, Marie, Kasper, FarMor, OnBankAccount
from emailing.models import UserPreferences, EmailQue
from django.contrib.auth.models import User
from django.apps import apps
from db_functions.transactions import get_db_entry, create_new_transaction


###############################
#   usernames and user IDs    #
###############################

def get_usernames(user_id):
  users = get_users()

  if isinstance(user_id, int):  # if type int = 1 value given
    for user in users:
      if user_id == user['id']:
        return user['username']
  else:                         # multiple values given e.g. [7, 8]
    """
    for userid in userdata: 
      for user in users: 
        if user['id'] == userid: 
          return user['username']
            """
    return [user['username'] for userid in user_id for user in users if user['id'] == userid]


def get_userIDs(username):
  users = get_users()

  if isinstance(username, str):     # if type int = 1 value given e.g. 'Kasper'
    for user in users:
        if username == user['username']:
          return user['id']         
  else:                             # multiple values given e.g. ['Kasper', 'Kirsten']
    return [user['id'] for user_name in username for user in users if user['username'] == user_name]


def get_users():
  users = User.objects.all()
  return [{'id': user.id, 'username': user.username} for user in users_data]


def request_user_IDs():
  users = get_users()
  return [user['id'] for user in users]




###############################
#        form CHOICES         #
###############################

def get_choices(user_groups):
  if user_groups.filter(name='ALL').exists():
    CHOICES=[(8,'Kirsten'),
            (9,'Marie'),
            (7,'Kasper'),
            (10,'Farmor & Farfar'),
            (11,'Gabriel'),
          ]
  elif user_groups.filter(name='FamNyhus').exists():
    CHOICES=[(8,'Kirsten'),
             (9,'Marie'),
             (7,'Kasper'),
             (10,'Farmor & Farfar'),
          ]
  elif user_groups.filter(name='Guests').exists():
    CHOICES=[(11,'Gabriel'),
          ]
  else:
    CHOICES=[]

  return CHOICES


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


###############################
#          User data          #
###############################

def _get_latest_entry(user_id):
    username = get_usernames(user_id)
    Model = apps.get_model('accounts', username)
    return Model.objects.latest('id')


def get_user_saldo(user_id):
    return _get_latest_entry(user_id).saldo


def get_user_km(user_id):
    return _get_latest_entry(user_id).km


def get_user_data(username):
    user_data = []

    Model = apps.get_model('accounts', username)
    
    db_data = Model.objects.all().order_by('-id')
    for entry in db_data:
        description = ''
        if entry.category == 'Udgift':
          udgift_data = get_db_entry(entry.transaction_id)
          description = udgift_data.description
        user_data.append({'date': entry.timestamp, 'saldo': entry.saldo, 'km': entry.km, 'category': entry.category, 'amount': entry.amount, 'description': description, 'transaction_id': entry.transaction_id })
   
    return user_data



###############################
#        User accounts        #
###############################

def update_user_account(transaction_id, user_id, amount, km, category):
    username = get_usernames(user_id)
    Model = apps.get_model('accounts', username)

    db_data = Model.objects.latest('id')
    new_saldo = db_data.saldo + amount
    new_km = db_data.km + km
    new_entry = Model(saldo=new_saldo, amount=amount, km=new_km, category=category, transaction_id=transaction_id)
    new_entry.save()
    

def update_accounts(request, form_data, category, km=0):
    new_id = create_new_transaction(request, category)
    
    user_list = form_data['user_id']
    user_ids = eval(user_list)
    
    if isinstance(user_ids, int):
        if category == 'Indskud':
          pass
        elif category == 'Tur':
          update_user_account(new_id, user_ids, form_data['amount'], km, category)
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
    username = get_user_info('get_user_names', user_id)
    Model = apps.get_model('accounts', username)
    
    #if user_id == 0:
    user_data = Model.objects.get(transaction_id=transaction_id)
    user_data.amount = amount
    user_data.save()
    _recalc_user_saldo(user_id)


def _update_user_km(transaction_id, user_id, delta_km):
    username = get_usernames(user_id)
    Model = apps.get_model('accounts', username)
    
    #if user_id == 0:
    user_data = Model.objects.get(transaction_id=transaction_id)
    try:
        prior_entry = Kirsten.objects.get(id=user_data.id - 1)
        last_km = prior_entry.km_count
        user_data.km_count = last_km + delta_km
        user_data.save()
        _recalc_user_saldo(user_id)
    except:
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