# from django.shortcuts import render

# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# import pickle
# import datetime


# SCOPES = ['https://www.googleapis.com/auth/calendar']


# def setupAPI():
#   flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
#   creds = flow.run_local_server(port=0)

#   pickle.dump(creds, open('token.pkl', 'wb'))

#   print('------------ SETUP API ------------')



# def bookings(request):
#     setupAPI()
    
#     creds = pickle.load(open('token.pkl', 'tb'))

#     service = build('calendar', 'v3', credentials=creds)

#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     print(events)
    
#     return render(request, 'bookings.html', context=events)