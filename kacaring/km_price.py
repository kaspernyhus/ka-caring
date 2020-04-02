from accounts.models import KmPrice

def get_km_price(user):

    if user.filter(name='VIP').exists():
      price = 1
    
    else:
      price = 2
    
    db_data = KmPrice.objects.get(pk=price)
    
    KM_PRICE = db_data.price

    return KM_PRICE