from accounts.models import Kirsten, Marie, Kasper, FarMor, OnBankAccount
from django.contrib.auth.models import User
from django.apps import apps
import db_functions


###############################
#   usernames and user IDs    #
###############################

def get_usernames(user_id):
  #print('User_id received: ', user_id, type(user_id))

  users = get_users()
  
  if isinstance(user_id, str):
    user_id = eval(user_id)
  
  if isinstance(user_id, int):  # if type int value given
    for user in users:
      if user_id == user['id']:
        #print('Users To Return: ', user['username'])
        return user['username']
  
  else:                         # multiple values given e.g. ['7', '8']
    user_list = [eval(user) for user in user_id]
    """
    for userid in userdata: 
      for user in users: 
        if user['id'] == userid: 
          return user['username']
            """
    users_toreturn = [user['username'] for userid in user_list for user in users if user['id'] == userid]
    # print('Users To Return: ', users_toreturn)
    return users_toreturn


def get_firstnames(user_id):
  users = get_users()
  users.append({'id': 0, 'username': 'Fælles-konto', 'first_name': 'Fælles-konto'})
  users.append({'id': 100, 'username': 'Tur_mangler', 'first_name': 'Tur mangler'})
  
  if isinstance(user_id, str):
    user_id = eval(user_id)
  
  if isinstance(user_id, int):  # if type int value given
    for user in users:
      if user_id == user['id']:
        return user['first_name']
  
  else:                         # multiple values given e.g. ['7', '8']
    user_list = [eval(user) for user in user_id]
    users_toreturn = [user['first_name'] for userid in user_list for user in users if user['id'] == userid]
    return users_toreturn



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
  
  return [{'id': user.id, 'username': user.username, 'first_name': user.first_name} for user in users]


def request_user_IDs(exclude=6):
  users = get_users()
  user_list = [user['id'] for user in users if not (user['id'] == exclude)]
  return user_list


def is_VIP(user):
    if user.groups.filter(name='VIP').exists():
      return True
    if user.groups.filter(name='ALL').exists():
      return True
    else:
      return False


###############################
#        form CHOICES         #
###############################

def get_choices(user_groups, tur=False, get_all=False):
  if get_all == True:
    CHOICES=[(8,'Kirsten'),
              (9,'Marie'),
              (7,'Kasper'),
              (10,'Farmor & Farfar'),
              (11,'Gabriel'),
            ]
    return CHOICES
  
  else:
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

    if tur==True:
        CHOICES.append((100,'Tur mangler',))

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


EKSTRA=[(0,''),
        (1,'Kirsten +1'),
        (2,'Marie +1'),
        (3,'Kasper +1'),
        (4,'Farmor & Farfar +1'),
        (5,'Kirsten +2'),
        (6,'Marie +2'),
        (7,'Kasper +2'),
        (8,'Farmor & Farfar +2')
        ]

###############################
#          User data          #
###############################

def _get_latest_entry(user_id):
    username = get_usernames(user_id)
    Model = apps.get_model('accounts', username)
    return Model.objects.latest('id')


def get_user_saldo(user_id):
    amount = _get_latest_entry(user_id).saldo
    if amount == 0:
      return 0
    else:
      return -amount


def get_user_km(user_id):
    return _get_latest_entry(user_id).km


def get_user_data(username):
    user_data = []

    Model = apps.get_model('accounts', username)
    
    db_data = Model.objects.all().order_by('-id')
    for entry in db_data:
        description = ''
        if entry.category == 'Indskud':
          indskud_data = db_functions.transactions.get_db_entry(entry.transaction_id)
          entry.amount = indskud_data.amount
        
        
        try:
          betaling_data = db_functions.transactions.get_db_entry(entry.transaction_id)
          description = betaling_data.description
        except:
          pass
        
        if entry.saldo == 0:
          saldo = 0
        else:
          saldo = -entry.saldo

        user_data.append({'date': entry.timestamp, 'saldo': saldo, 'km': entry.km, 'category': entry.category, 'amount': entry.amount, 'description': description, 'transaction_id': entry.transaction_id })
   
    return user_data


