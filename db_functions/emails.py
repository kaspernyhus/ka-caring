from emailing.models import EmailPreferences, EmailQue


###############################
#        email PREFs          #
###############################

def get_email_prefs(user_id):
  db_data = EmailPreferences.objects.get(user_id=user_id)
  
  email_prefs = []

  if db_data.monthly_saldo:
    email_prefs.append(0)
  if db_data.udgift_oprettet:
    email_prefs.append(1)
  if db_data.tankning_oprettet:
    email_prefs.append(2)
  if db_data.tur_oprettet:
    email_prefs.append(3)
  if db_data.indbetaling_oprettet:
    email_prefs.append(4)

  return email_prefs


def update_email_prefs(user_id, form_data):
  db_data = EmailPreferences.objects.get(user_id=user_id)
  
  db_data.monthly_saldo = False
  db_data.udgift_oprettet = False
  db_data.ankning_oprettet = False
  db_data.tur_oprettet = False

  form_data = eval(form_data['user_prefs'])

  for checkbox in form_data:
    if checkbox == '0':
      db_data.monthly_saldo = True
    if checkbox == '1':
      db_data.udgift_oprettet = True
    if checkbox == '2':
      db_data.ankning_oprettet = True
    if checkbox == '3':
      db_data.tur_oprettet = True

  db_data.save()


###############################
#          email Que          #
###############################

def get_email_que():
  db_data = EmailQue.objects.get(id=1)
  return eval(db_data.email_que)


def update_email_que(data):
  db_data = EmailQue.objects.get(id=1)
  db_data.email_que = data
  db_data.save()