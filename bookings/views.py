from django.shortcuts import render

#from apiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow

def bookings(request):
    return render(request, 'bookings.html')