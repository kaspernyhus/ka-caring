from django.shortcuts import render, redirect
from kacaring.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from datetime import datetime, timedelta, time
from django.views.generic import TemplateView
from .forms import UserPrefForm
from db_functions.emails import get_email_prefs, update_email_prefs, get_email_que, update_email_que
from db_functions.users import request_user_IDs, get_usernames, get_firstnames
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class UserPref(TemplateView):
    template_name = 'emailing/user_pref.html'

    def get(self, request):
        form = UserPrefForm(request.user)
        form.fields['user_prefs'].initial = get_email_prefs(request.user.id)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserPrefForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_obj = User.objects.get(id=request.user.id)
            user_obj.email = data['email']
            user_obj.save()
            
            update_email_prefs(request.user.id, data)
        else:
            update_email_prefs(request.user.id, {'user_prefs': "[]"})
        return redirect('/')


def send_mail_to_user(user_id, subject, message):
  user = User.objects.get(id=user_id)
  recepient = user.email
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

  for user in request_user_IDs():
    email_pref = get_email_prefs(user)
    
    for pref in email_pref:
      if pref == 0:
        amount = round(get_saldo(user), 2)
        username = get_firstnames(user)
        message = 'Hej ' + username + ',\n \nDu skylder Ford-KA\'ssen: ' + str(amount) + ' kr. \n MobilePay til Kasper på 61681287 og husk at registrer det i App\'en. \n \n Mvh \nFord Ka Kørsel aps'
        
        if amount != 0:
          send_mail_to_user(user, subject, message)


def add_to_mail_Q(username, data, category):
  if category == 'Udgift':
    subject = 'Ford Ka Kørsel - Udgift registreret'
    message = 'd. ' + data['date'].strftime("%d/%m/%y") + ' har ' + username + ' oprettet en udgift på ' + str(round(data['amount'], 2)) + ' kr. med teksten:\n' + data['description'] + '.\n \n Mvh \nFord Ka Kørsel aps'
  elif category == 'Tankning':
    subject = 'Ford Ka Kørsel - Tankning registreret'
    message = 'd. ' + data['date'].strftime("%d/%m/%y") + ' har ' + username + ' registreret en tankning på ' + str(round(data['amount'], 2)) + ' kr.\n \n Mvh \nFord Ka Kørsel aps'
  elif category == 'Tur':
    subject = 'Ford Ka Kørsel - Tur registreret'
    message = 'd. ' + data['date'].strftime("%d/%m/%y") + ' har ' + username + ' registreret en tur.\nAktuel km-tæller: ' + str(data['km_count']) + ' km.\n \n Mvh \nFord Ka Kørsel aps'
  elif category == 'Indbetaling':
    subject = 'Ford Ka Kørsel - Indbetaling registreret'
    message = 'd. ' + data['date'].strftime("%d/%m/%y") + ' har ' + username + ' registreret en indbetaling fra ' + str(get_usernames(data['user_id'])) + ' (userID: ' + str(data['user_id']) + ') på ' + str(data['amount']) + ' kr.\n \n Mvh \nFord Ka Kørsel aps'
  
  if subject and message:
    for user in request_user_IDs(exclude=0):
      email_pref = get_email_prefs(user)

      for pref in email_pref:
        if category == 'Udgift' and pref == 1:
          email = {'user_id': user, 'subject': subject, 'message': message}
          emailQue_add(email)
        if category == 'Tankning' and pref == 2:
          email = {'user_id': user, 'subject': subject, 'message': message}
          emailQue_add(email)
        if category == 'Tur' and pref == 3:
          email = {'user_id': user, 'subject': subject, 'message': message}
          emailQue_add(email)
        if category == 'Indbetaling' and pref == 4:
          email = {'user_id': user, 'subject': subject, 'message': message}
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
  next_month = any_day.replace(day=28) + timedelta(days=4)
  return next_month - timedelta(days=next_month.day)


def check_email_scheduler(request):
  today = datetime.now()
  ldom = last_day_of_month(today.date())

  if today.time() > time(8,00) and today.time() < time(9,00):
    if today.date() == ldom:
      send_monthly_saldo_mail()

  send_all_mails_in_Q()

  return render(request, 'emailing/mail_send.html')