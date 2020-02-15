from django.urls import path

from . import views


urlpatterns = [
    path('', views.oversigt, name='oversigt'),
    path('alle_transaktioner', views.show_all_transactions, name='show_all_transactions'),
    # path('transactionID<int:transaction_id>', views.edit_entry, name='edit_entry'),
    path('kasper', views.show_user_transactions, name='show_user_transactions'),
]
