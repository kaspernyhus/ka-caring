from django.urls import path

from . import views

urlpatterns = [
    path('oversigt', views.oversigt, name='oversigt')
]
