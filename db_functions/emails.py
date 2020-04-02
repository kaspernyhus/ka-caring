from accounts.models import TransactionId
from ture.models import Ture
from tbu.models import Tankning, Betaling, Udgift
from datetime import datetime
from accounts.models import Kirsten, Marie, Kasper, FarMor, OnBankAccount
from emailing.models import UserPreferences, EmailQue
from django.contrib.auth.models import User
from django.apps import apps
import accounts


def get_email_prefs(user_id):
  db_data = UserPreferences.objects.get(id=1)
  
  monthly_saldo = eval(db_data.monthly_saldo)
  udgift_oprettet = eval(db_data.udgift_oprettet)
  tankning_oprettet = eval(db_data.tankning_oprettet)
  tur_oprettet = eval(db_data.tur_oprettet)

  email_prefs = []

  if monthly_saldo[user_id]:
    email_prefs.append(0)
  if udgift_oprettet[user_id]:
    email_prefs.append(1)
  if tankning_oprettet[user_id]:
    email_prefs.append(2)
  if tur_oprettet[user_id]:
    email_prefs.append(3)

  return email_prefs


def update_email_prefs(user_id, form_data):
  db_data = UserPreferences.objects.get(id=1)
  
  monthly_saldo = eval(db_data.monthly_saldo)
  udgift_oprettet = eval(db_data.udgift_oprettet)
  tankning_oprettet = eval(db_data.tankning_oprettet)
  tur_oprettet = eval(db_data.tur_oprettet)

  monthly_saldo[user_id] = 0
  udgift_oprettet[user_id] = 0
  tankning_oprettet[user_id] = 0
  tur_oprettet[user_id] = 0

  form_data = eval(form_data['user_prefs'])

  for checkbox in form_data:
    if checkbox == '0':
      monthly_saldo[user_id] = 1
    
    if checkbox == '1':
      udgift_oprettet[user_id] = 1
    
    if checkbox == '2':
      tankning_oprettet[user_id] = 1
    
    if checkbox == '3':
      tur_oprettet[user_id] = 1

  db_data.monthly_saldo = monthly_saldo
  db_data.udgift_oprettet = udgift_oprettet
  db_data.tankning_oprettet = tankning_oprettet
  db_data.tur_oprettet = tur_oprettet
  db_data.save()


def get_email_que():
  db_data = EmailQue.objects.get(id=1)
  return eval(db_data.email_que)


def update_email_que(data):
  db_data = EmailQue.objects.get(id=1)
  db_data.email_que = data
  db_data.save()