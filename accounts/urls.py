from django.urls import path

from . import views

urlpatterns = [
    path('', views.oversigt, name='oversigt'),
    path('alle_transaktioner', views.show_all_transactions, name='show_all_transactions')
]
