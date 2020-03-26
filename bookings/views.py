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
from datetime import datetime, timedelta
from django.views.generic import TemplateView
from .forms import BookingForm
from db_functions.db_data import get_userID, get_usernames


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


def get_calendar_events():
  credentials = CredentialsModel.objects.get(id=1)
  service = build('calendar', 'v3', credentials=credentials.credential)
  calendar_list_entry = service.calendarList().list().execute()
  calendar_id = calendar_list_entry['items'][0]['id']

  current_date = datetime.now().date()
  _2_weeks_ago = datetime.now() - timedelta(14)
  _2_weeks_ago = str(_2_weeks_ago.date()) + 'T00:00:00Z'

  calendar_events = service.events().list(calendarId=calendar_id, timeMin=_2_weeks_ago).execute()

  events = []

  for calendar_event in calendar_events['items']:
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 1, 1)

    try:
      start_date = datetime.strptime(calendar_event['start']['date'], '%Y-%m-%d').date()
    except:
      pass
    try:
      start_date = datetime.strptime(calendar_event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z').date()
    except:
      pass
    
    try:
      end_time = datetime.strptime(calendar_event['end']['date'], '%Y-%m-%d')
      end_time = end_time - timedelta(1)
      end_date = end_time.date()
    except:
      pass
    try:
      end_time = datetime.strptime(calendar_event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z').date()
      end_time = end_time - timedelta(1)
      end_date = end_time.date()
    except:
      pass
    
    if end_date >= current_date:
      event = {'summary': calendar_event['summary'], 'start': start_date.strftime('%d/%m/%y'), 'end': end_date.strftime('%d/%m/%y')}
      current_date = datetime.now().date()
      events.append(event)

  return events  


def show_bookings(request):
  calendar_events = get_calendar_events()
  context = {'events': calendar_events}
  return render(request, 'show_bookings.html', context=context)


def check_if_booked(start_date, end_date):
  bookings = get_calendar_events()
  
  start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
  end_date = datetime.strptime(str(end_date), '%Y-%m-%d')

  for booking in bookings:
    booking_start = datetime.strptime(booking['start'], '%d/%m/%y')
    booking_end = datetime.strptime(booking['end'], '%d/%m/%y')

    if start_date >= booking_start and start_date <= booking_end:
      return True
    elif end_date >= booking_start and end_date <= booking_end:
      return True
  
  return False


def create_calendar_event(start_date, end_date, username):
  credentials = CredentialsModel.objects.get(id=1)
  service = build('calendar', 'v3', credentials=credentials.credential)

  end_date = end_date + timedelta(1)

  event = {
  'summary': username,
  'description': 'Booking af Ford KA',
  'start': {
    'date': start_date.strftime("%Y-%m-%d"),
    'timeZone': 'Europe/Copenhagen',
  },
  'end': {
    'date': end_date.strftime("%Y-%m-%d"),
    'timeZone': 'Europe/Copenhagen',
  },
  'reminders': {'useDefault': False},
  }
  
  event = service.events().insert(calendarId='ford.ka.korsel@gmail.com', body=event).execute()


def create_booking(request):
  form = BookingForm()
  form.fields['user_id'].initial = get_userID(request.user.username)

  if request.method == 'POST':
    form = BookingForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      start_date = data['start_date']
      end_date = data['end_date']
      username = get_usernames(data['user_id'])
      

      if check_if_booked(start_date, end_date):
        OBS = 1
      else:
        OBS = 0
      
      create_calendar_event(start_date, end_date, username)
      
      return render(request, 'event_created.html', context={'user': username, 'start_date': start_date.strftime("%d/%m/%Y") , 'end_date': end_date.strftime("%d/%m/%Y"), 'OBS': OBS})

  return render(request, 'create_event.html', context={'form': form})

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