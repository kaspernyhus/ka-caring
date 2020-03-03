from django.shortcuts import render
from kacaring.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from datetime import datetime

from db_functions.db_data import get_saldo


def mail_to_users(request):
    now = datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")

    if month == 'January':
        month = 'Januar'
    if month == 'February':
        month = 'Februar'
    if month == 'March':
        month = 'Marts'
    if month == 'April':
        month = 'April'
    if month == 'May':
        month = 'Maj'
    if month == 'June':
        month = 'Juni'
    if month == 'July':
        month = 'Juli'
    if month == 'August':
        month = 'August'
    if month == 'September':
        month = 'September'
    if month == 'October':
        month = 'Oktober'
    if month == 'November':
        month = 'November'
    if month == 'December':
        month = 'December'


    for user in range(4):
        amount = get_saldo(user)
        subject = 'Ford Ka Kørsel - ' + month + ' ' + year
        
        if user == 0:
            recepient = 'kanyhus@gmail.com'
            message = 'Hej Kirsten,\n \nDu skylder Ford-fælles-kassen: ' + str(amount) + ' kr. \n MobilePay her <link> og husk at registrer det i App\'en. \n \n Mvh \nFord Ka Kørsel aps'
        elif user == 1:
            recepient = 'kanyhus@gmail.com'
            message = 'Hej Marie,\n \nDu skylder Ford-fælles-kassen: ' + str(amount) + ' kr. \n MobilePay her <link> og husk at registrer det i App\'en. \n \n Mvh \nFord Ka Kørsel aps'
        elif user == 2:
            recepient = 'kanyhus@gmail.com'
            message = 'Hej Kasper,\n \nDu skylder Ford-fælles-kassen: ' + str(amount) + ' kr. \n MobilePay her <link> og husk at registrer det i App\'en. \n \n Mvh \nFord Ka Kørsel aps'
        elif user == 3:
            recepient = 'kanyhus@gmail.com'
            message = 'Hej Farmor & Farfar,\n \nI skylder Ford-fælles-kassen: ' + str(amount) + ' kr. \n MobilePay her <link> og husk at registrer det i App\'en. \n \n Mvh \nFord Ka Kørsel aps'
        else:
            recepient = 'kanyhus@gmail.com'
            message = 'for meget'

        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    
    return render(request, 'mail_send.html')