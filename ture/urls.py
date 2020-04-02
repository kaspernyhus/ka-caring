from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', login_required(login_url='login')(views.CreateTur.as_view()), name='create_tur'),
    path('update/<int:pk>/', login_required(login_url='login')(views.TurUpdate.as_view()), name='update_tur'),
]
