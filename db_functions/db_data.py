from tur.models import Ture

def get_usernames(id_list):
    users = ['Kirsten','Marie','Kasper','Ukendt']
    active_users = eval(id_list)

    print(isinstance(active_users, int))
    if isinstance(active_users, int):
        return users[active_users]
    else:
        active_users = eval(id_list)
        user_names = [users[int(user)] for user in active_users]
        return user_names
      
    

def get_current_km():
    db_data = Ture.objects.latest('id')
    return db_data.km_count