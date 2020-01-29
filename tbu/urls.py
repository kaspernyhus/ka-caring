from django.urls import path

from . import views

urlpatterns = [
    path('tankning', views.CreateTankning.as_view(), name='create_tankning'),
    path('betaling', views.CreateBetaling.as_view(), name='create_betaling'),
    path('udgift', views.CreateUdgift.as_view(), name='create_udgift')
]
