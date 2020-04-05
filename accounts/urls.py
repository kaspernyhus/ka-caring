from django.urls import path

from . import views


urlpatterns = [
    path('', views.oversigt, name='oversigt'),
    path('guest_oversigt', views.guest_oversigt, name='guest_oversigt'),
    path('alle_transaktioner', views.show_all_transactions, name='show_all_transactions'),
    path('<str:username>/', views.show_user_transactions, name='show_user_transactions'),
    path('delete_trans/<int:pk>/', views.TransactionDelete.as_view(), name='delete_trans'),
]
