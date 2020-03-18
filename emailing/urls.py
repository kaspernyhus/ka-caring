from django.urls import path

from . import views

urlpatterns = [
    path('user_pref', views.UserPref.as_view(), name='user_pref'),
    path('check_scheduler', views.check_email_scheduler, name='check_scheduler')
]