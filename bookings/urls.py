from django.conf.urls import url
from django.urls import path
from . import views 

urlpatterns = [ 
	url(r'^googleAuthenticate', views.google_authenticate, name ='google_authenticate'), 
	url(r'^oauth2callback', views.auth_return), 
	url(r'^login', views.login, name ='login'),
  path('', views.show_bookings, name='show_bookings'),
  path('create_booking', views.create_booking, name='create_booking'),
  
] 
