from django.shortcuts import render
from kacaring.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from datetime import datetime

from db_functions.db_data import get_saldo


def mail_to_users(request):
    now = datetime.now()

    for user in range(4):
        amount = get_saldo(user)
        subject = 'Ford Ka Kørsel' + now.strftime("%m")
        
        if user == 0:
            recepient = 'kanyhus@gmail.com'
            message = 'Hej Kirsten, du skylder Ford-fælles-kassen: ' + str(amount) + ' kr. Venligst mobilepay til: 12 34 56 78'
        elif user == 1:
            recepient = 'kanyhus@gmail.com'
            message = 'Hej Marie, du skylder Ford-fælles-kassen: ' + str(amount) + ' kr. Venligst mobilepay til: 12 34 56 78'
        elif user == 2:
            recepient = 'kanyhus@gmail.com'
            message = 'Hej Kasper, du skylder Ford-fælles-kassen: ' + str(amount) + ' kr. Venligst mobilepay til: 12 34 56 78'
        elif user == 3:
            recepient = 'kanyhus@gmail.com'
            message = 'Hej FarMor, du skylder Ford-fælles-kassen: ' + str(amount) + ' kr. Venligst mobilepay til: 12 34 56 78'
        else:
            recepient = 'kanyhus@gmail.com'
            message = 'for meget'

        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    
    return render(request, 'mail_send.html', {'recepient': recepient})