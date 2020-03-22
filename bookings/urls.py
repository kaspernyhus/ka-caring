from django.conf.urls import url
from django.urls import path
from . import views 

urlpatterns = [ 
	url(r'^googleAuthenticate', views.google_authenticate, name ='google_authenticate'), 
	url(r'^oauth2callback', views.auth_return), 
	url(r'^login', views.login, name ='login'),
  path('', views.calendar, name='calendar'),
] 
