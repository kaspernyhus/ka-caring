from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('tankning', login_required(login_url='login')(views.CreateTankning.as_view()), name='create_tankning'),
    path('betaling', login_required(login_url='login')(views.CreateBetaling.as_view()), name='create_betaling'),
    path('udgift', login_required(login_url='login')(views.CreateUdgift.as_view()), name='create_udgift'),
    path('admin_udgift', login_required(login_url='login')(views.CreateAdminUdgift.as_view()), name='create_admin_udgift'),
    path('udbetaling', login_required(login_url='login')(views.CreateUdbetaling.as_view()), name='create_udbetaling'),
    path('tankning/update/<int:pk>', login_required(login_url='login')(views.TankningUpdate.as_view()), name='update_tankning'),
    path('betaling/update/<int:pk>', login_required(login_url='login')(views.BetalingUpdate.as_view()), name='update_betaling'),
    path('udgift/update/<int:pk>', login_required(login_url='login')(views.UdgiftUpdate.as_view()), name='update_udgift'),
]

