from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateTankning.as_view(), name='create_tankning'),
]
