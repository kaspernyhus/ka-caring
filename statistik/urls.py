from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_stats, name='statistik'),
    path('FAQ', views.faq, name='FAQ'),
]

