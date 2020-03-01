from django.urls import path

from . import views


urlpatterns = [
    path('send', views.mail_to_users, name='send_email'),
]