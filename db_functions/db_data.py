from tur.models import Ture

def get_usernames(form_data):
    users = ['Kirsten','Marie','Kasper','Ukendt']
    active_users = eval(form_data['user_id'])
      
    user_names = [users[int(user)] for user in active_users]
    return user_names

def get_current_km():
    db_data = Ture.objects.latest('id')
    return db_data.km_count