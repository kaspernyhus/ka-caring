from django.shortcuts import render
from db_functions.users import get_user_km, is_VIP, request_user_IDs, get_usernames, get_firstnames, get_total_user_km
from db_functions.transactions import get_current_km, get_total_tankning, get_total_km, get_total_udgift
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required(login_url='login')
@user_passes_test(is_VIP, login_url='guest_stats')
def show_stats(request):
  context = {'total_km': get_total_km ,'benzinpris_pr_km': calc_km_fuel_price(), 'usage': calc_usage()[:-1], 'pris_pr_km': calc_expenses_pr_km, 'total_expense': get_total_udgift}
  return render(request, 'oversigter/stats.html', context)


def show_guest_stats(request):
  context = {'total_km': get_total_km}
  return render(request, 'oversigter/guest_stats.html', context)


def calc_km_fuel_price():
  try:
    km = get_total_km()
    tankning = get_total_tankning()
    pris_pr_km = tankning / km
  except:
    pris_pr_km = 0.0
  return pris_pr_km


def calc_usage():
  total_km = get_total_user_km()
  print("total km:", total_km)
  
  usage = []

  for user_id in request_user_IDs():
    user_km = get_user_km(user_id)
    print("userkm:", user_km)
    user_usage = (user_km / total_km) * 100
    print("userusage:", user_usage)
    user = {'id': user_id, 'username': get_firstnames(user_id), 'km': user_km, 'usage': round(user_usage, 1)}
    usage.append(user)
  return usage


def calc_expenses_pr_km():
  tankninger = get_total_tankning()
  udgifter = get_total_udgift()
  total_expenses = tankninger + udgifter
  km = get_total_km()

  pris_pr_km = total_expenses / km

  return pris_pr_km


@login_required(login_url='login')
def faq(request):
  return render(request, 'oversigter/faq.html')

@login_required(login_url='login')
def vejhjaelp(request):
  return render(request, 'oversigter/vejhjaelp.html')

@login_required(login_url='login')
def forsikring(request):
  return render(request, 'oversigter/forsikring.html')