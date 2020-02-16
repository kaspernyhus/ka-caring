from django.urls import path

from . import views


urlpatterns = [
    path('', views.oversigt, name='oversigt'),
    path('alle_transaktioner', views.show_all_transactions, name='show_all_transactions'),
    path('<str:userIDname>/', views.show_user_transactions, name='show_user_transactions'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
]
