from accounts.models import KmPrice

def get_km_price():

    db_data = KmPrice.objects.get(pk=1)

    KM_PRICE = db_data.price

    return KM_PRICE