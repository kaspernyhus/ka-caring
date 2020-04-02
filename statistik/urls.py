from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_stats, name='statistik'),
    path('guest_stats', views.show_guest_stats, name='guest_stats'),
    path('FAQ', views.faq, name='FAQ'),
]

