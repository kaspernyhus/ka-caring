from ture.models import Ture
from tbu.models import Tankning, Betaling, Udgift
from datetime import datetime
from accounts.models import Kirsten, Marie, Kasper
from kacaring.km_price import km_price 


def get_usernames(id_list):
    users = ['Kirsten','Marie','Kasper','Ukendt']
    active_users = eval(id_list)

    if isinstance(active_users, int):
        return users[active_users]
    else:
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


def get_all_data():
    all_data = []

    ture = Ture.objects.all().order_by('-id')
    for tur in ture:
        all_data.append({'date': tur.date, 'km_count': tur.km_count, 'users': get_usernames(tur.user_id), 'type': 'Kørsel'})
    
    tankninger = Tankning.objects.all().order_by('-id')
    for tankning in tankninger:
        all_data.append({'date': tankning.date, 'amount': tankning.amount, 'users': [get_usernames(tankning.user_id)], 'type': 'Tankning'})
    
    betalinger = Betaling.objects.all().order_by('-id')
    for betaling in betalinger:
        all_data.append({'date': betaling.date, 'amount': betaling.amount, 'users': [get_usernames(betaling.user_id)], 'type': 'Betaling'})
    
    udgifter = Udgift.objects.all().order_by('-id')
    for udgift in udgifter:
        all_data.append({'date': udgift.date, 'amount': udgift.amount, 'description': udgift.description, 'users': [get_usernames(udgift.user_id)], 'type': 'Udgift'})
    
    all_data_sorted = sorted(all_data, key=lambda k: k['date'], reverse=True)
    return all_data_sorted


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
