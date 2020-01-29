from ture.models import Ture
from datetime import datetime
from accounts.models import Kirsten, Marie, Kasper


def get_usernames(id_list):
    users = ['Kirsten','Marie','Kasper','Ukendt']
    active_users = eval(id_list)

    if isinstance(active_users, int):
        return users[active_users]
    else:
        active_users = eval(id_list)
        user_names = [users[int(user)] for user in active_users]
        return user_names
         

def get_current_km():
    db_data = Ture.objects.latest('id')
    return db_data.km_count
    


def get_saldo(user_id):
    if user_id == 0:
        db_data = Kirsten.objects.latest('id')
    elif user_id == 1:
        db_data = Marie.objects.latest('id')
    elif user_id == 2:
        db_data = Kasper.objects.latest('id')
    return db_data.saldo


def get_user_km(user_id):
    if user_id == 0:
        db_data = Kirsten.objects.latest('id')
    elif user_id == 1:
        db_data = Marie.objects.latest('id')
    elif user_id == 2:
        db_data = Kasper.objects.latest('id')
    return db_data.km


def update_saldo(user_id, amount):
    print('----------- update saldo --------------')
    user_id = eval(user_id)
    timestamp = datetime.now()

    if user_id == 0:
        db_data = Kirsten.objects.latest('id')
        new_saldo = db_data.saldo + amount
        km = get_user_km(0)
        new_entry = Kirsten(timestamp=timestamp, saldo=new_saldo, km=km)
        new_entry.save()
        print('----------- Kirsten --------------')
        
    elif user_id == 1:
        db_data = Marie.objects.latest('id')
        new_saldo = db_data.saldo + amount
        km = get_user_km(1)
        new_entry = Marie(timestamp=timestamp, saldo=new_saldo, km=km)
        new_entry.save()
        print('----------- Marie --------------')

    elif user_id == 2:
        db_data = Kasper.objects.latest('id')
        new_saldo = db_data.saldo + amount
        km = get_user_km(2)
        new_entry = Kasper(timestamp=timestamp, saldo=new_saldo, km=km)
        new_entry.save()
        print('----------- Kasper --------------')


def update_account(user_id, amount, km):
    print('----------- update account --------------')
    timestamp = datetime.now()
    user_id = eval(user_id)

    for user in user_id:
        user = int(user)
        if user == 0:
            db_data = Kirsten.objects.latest('id')
            new_saldo = db_data.saldo + amount
            new_km = db_data.km + km
            new_entry = Kirsten(timestamp=timestamp, saldo=new_saldo, km=new_km)
            new_entry.save()
            print('----------- Kirsten --------------')
            
        elif user == 1:
            db_data = Marie.objects.latest('id')
            new_saldo = db_data.saldo + amount
            new_km = db_data.km + km
            new_entry = Marie(timestamp=timestamp, saldo=new_saldo, km=new_km)
            new_entry.save()
            print('----------- Marie --------------')

        elif user == 2:
            db_data = Kasper.objects.latest('id')
            new_saldo = db_data.saldo + amount
            new_km = db_data.km + km
            new_entry = Kasper(timestamp=timestamp, saldo=new_saldo, km=new_km)
            new_entry.save()
            print('----------- Kasper --------------')
