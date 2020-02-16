from django.urls import path

from . import views

urlpatterns = [
    path('tankning', views.CreateTankning.as_view(), name='create_tankning'),
    path('betaling', views.CreateBetaling.as_view(), name='create_betaling'),
    path('udgift', views.CreateUdgift.as_view(), name='create_udgift'),
    path('tankning/update/<int:pk>', views.TankningUpdate.as_view(), name='update_tankning'),
    path('betaling/update/<int:pk>', views.BetalingUpdate.as_view(), name='update_betaling'),
    path('udgift/update/<int:pk>', views.UdgiftUpdate.as_view(), name='update_udgift'),
]

