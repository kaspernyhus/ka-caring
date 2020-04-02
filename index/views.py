from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from db_functions.transactions import get_current_km


@login_required(login_url='login')
def index(request):
  current_km = get_current_km()
  return render(request, 'users/index.html', {'current_km': current_km})
