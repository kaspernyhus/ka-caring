import httplib2

from googleapiclient.discovery import build
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from .models import CredentialsModel
from kacaring import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.shortcuts import render
from httplib2 import Http
from datetime import datetime

def login(request):
    status = True

    
    try:
        storage = DjangoORMStorage(CredentialsModel, 'id', 1, 'credential')
        credential = storage.get()
        access_token = credential.access_token
        resp, cont = Http().request("https://www.googleapis.com/auth/calendar",
                                    headers={'Host': 'www.googleapis.com',
                                            'Authorization': access_token})
    except:
        status = False
        print('Not Found')

    return render(request, 'google_login.html', {'status': status})


def calendar(request):
  
  credentials = CredentialsModel.objects.get(id=1)
  
  service = build('calendar', 'v3', credentials=credentials.credential)
  
  calendar_list_entry = service.calendarList().list().execute()

  calendar_id = calendar_list_entry['items'][0]['id']
  calendar_events = service.events().list(calendarId=calendar_id).execute()

  #print(calendar_events)

  

  events = []

  for calendar_event in calendar_events['items']:
    start_date = datetime.strptime(calendar_event['start']['date'], '%Y-%m-%d')
    end_date = datetime.strptime(calendar_event['end']['date'], '%Y-%m-%d')
    event = {'summary': calendar_event['summary'], 'start': start_date.strftime('%d/%m/%y'), 'end': end_date.strftime('%d/%m/%y')}
    
    current_date = datetime.now().date()

    if start_date.date() > current_date:
      events.append(event)

  context = {'events': events}

  return render(request, 'show_bookings.html', context=context)


################################
#   GMAIL API IMPLEMENTATION   #
################################

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://kacaring.pythonanywhere.com/bookings/oauth2callback', #localhost:8000
    prompt='consent')


def google_authenticate(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', 1, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('calendar', 'v3', http=http)
        print('access_token = ', credential.access_token)
        status = True

        return render(request, 'google_login.html', {'status': status})


def auth_return(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET.get('code'))
    storage = DjangoORMStorage(CredentialsModel, 'id', 1, 'credential')
    storage.put(credential)
    print("access_token: %s" % credential.access_token)
    return HttpResponseRedirect("/")