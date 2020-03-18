from django.shortcuts import render, redirect
from kacaring.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from datetime import datetime, timedelta, time
from django.views.generic import TemplateView
from .forms import UserPrefForm
from db_functions.db_data import get_saldo, get_email_prefs, update_email_prefs, get_userID, get_usernames, get_email_que, update_email_que


class UserPref(TemplateView):
    template_name = 'user_pref.html'

    def get(self, request):
        form = UserPrefForm()
        user_id = get_userID(request.user.username)
        print(user_id)
        form.fields['user_prefs'].initial = get_email_prefs(0)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserPrefForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user_id = get_userID(request.user.username)
            update_email_prefs(user_id, data)
        else:
            user_id = get_userID(request.user.username)
            update_email_prefs(user_id, {'user_prefs': "[]"})
        return redirect('index')


def send_mail_to_user(user_id, subject, message):
  if user_id == 0:
    recepient = 'kanyhus@gmail.com' #nyhuskirsten@gmail.com
  elif user_id == 1:
    recepient = 'kanyhus@gmail.com' #marienyhusjanssen@gmail.com
  elif user_id == 2:
    recepient = 'kanyhus@gmail.com'
  elif user_id == 3:
    recepient = 'kanyhus@gmail.com' #janssen.per@gmail.com
  elif user_id == 4:
    recepient = 'ford.ka.korsel@gmail.com'
  else:
    recepient = 'ford.ka.korsel@gmail.com'
    message = 'email failed\n' + message
  
  send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)


def send_monthly_saldo_mail():
  now = datetime.now()
  month = now.strftime("%B")
  year = now.strftime("%Y")

  if month == 'January':
    month = 'Januar'
  if month == 'February':
    month = 'Februar'
  if month == 'March':
    month = 'Marts'
  if month == 'May':
    month = 'Maj'
  if month == 'June':
    month = 'Juni'
  if month == 'July':
    month = 'Juli'
  if month == 'October':
    month = 'Oktober'
  
  subject = 'Ford Ka Kørsel - ' + month + ' ' + year

  for user in range(4):
    email_pref = get_email_prefs(user)
    
    for pref in email_pref:
      if pref == 0:
        amount = round(get_saldo(user), 2)
        username = get_usernames(str(user))
        message = 'Hej ' + username + ',\n \nDu skylder Ford-KA\'ssen: ' + str(amount) + ' kr. \n MobilePay til Kasper på 61681287 og husk at registrer det i App\'en. \n \n Mvh \nFord Ka Kørsel aps'

        send_mail_to_user(user, subject, message)


def udgift_oprettet_mail(username, data):
  subject = 'Ford Ka Kørsel - Udgift registreret'
  
  for user in range(4):
    email_pref = get_email_prefs(user)

    for pref in email_pref:
      if pref == 1:
        message = 'd. ' + str(data['date']) + ' har ' + username + ' oprettet en udgift på ' + str(round(data['amount'], 2)) + ' kr. med teksten:\n' + data['description'] + '.\n \n Mvh \nFord Ka Kørsel aps'
        email = {'user_id': user, 'subject': subject, 'message': message}
        emailQue_add(email)
  email = {'user_id': 4, 'subject': subject, 'message': message}
  emailQue_add(email)


def tankning_oprettet_mail(username, data):
  subject = 'Ford Ka Kørsel - Tankning registreret'
  
  for user in range(4):
    email_pref = get_email_prefs(user)

    for pref in email_pref:
      if pref == 2:
        message = 'd. ' + str(data['date']) + ' har ' + username + ' registreret en tankning på ' + str(round(data['amount'], 2)) + ' kr.\n \n Mvh \nFord Ka Kørsel aps'
        email = {'user_id': user, 'subject': subject, 'message': message}
        emailQue_add(email)
  email = {'user_id': 4, 'subject': subject, 'message': message}
  emailQue_add(email)


def tur_oprettet_mail(username, data):
  subject = 'Ford Ka Kørsel - Tur registreret'
  
  for user in range(4):
    email_pref = get_email_prefs(user)

    for pref in email_pref:
      if pref == 3:
        message = 'd. ' + str(data['date']) + ' har ' + username + ' registreret en tur.\nAktuel km-tæller: ' + str(data['km_count']) + ' km.\n \n Mvh \nFord Ka Kørsel aps'
        email = {'user_id': user, 'subject': subject, 'message': message}
        emailQue_add(email)
  email = {'user_id': 4, 'subject': subject, 'message': message}
  emailQue_add(email)


def indbetaling_oprettet_mail(username, data):
  subject = 'Ford Ka Kørsel - Indbetaling registreret'
  message = 'd. ' + str(data['date']) + ' har ' + username + ' registreret en indbetaling fra ' + str(get_usernames(data['user_id'])) + ' (userID: ' + str(data['user_id']) + ') på ' + str(data['amount']) + ' kr.\n \n Mvh \nFord Ka Kørsel aps'
  email = {'user_id': 4, 'subject': subject, 'message': message}
  emailQue_add(email)


def emailQue_add(data):
  emailQue = get_email_que()
  emailQue.append(data)
  update_email_que(emailQue)


def emailQue_clear():
  update_email_que("[]")
  

def send_all_mails_in_Q():
  emailQue = get_email_que()
  for email in emailQue:
    send_mail_to_user(email['user_id'], email['subject'], email['message'])
  emailQue_clear()
  

#######################
#      Scheduler      #
#######################

def last_day_of_month(any_day):
  next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
  return next_month - timedelta(days=next_month.day)


def check_email_scheduler(request):
  today = datetime.now()
  ldom = last_day_of_month(today.date())

  if today.time() > time(8,00) and today.time() < time(9,00):
    if today.date() == ldom:
      send_monthly_saldo_mail()

  send_all_mails_in_Q()

  return render(request, 'mail_send.html')