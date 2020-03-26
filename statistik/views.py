from django.shortcuts import render
from db_functions.db_data import get_total_tankning, get_current_km, get_user_km


def get_total_km():
  km = get_current_km()
  km = km - 114293 #km ved overtagelse
  return km


def show_stats(request):
  context = {'total_km': get_total_km ,'pris_pr_km': calc_km_fuel_price(), 'usage': calc_usage() }
  return render(request, 'oversigter/stats.html', context)


def calc_km_fuel_price():
  try:
    km = get_total_km()
    tankning = get_total_tankning()
    pris_pr_km = tankning / km
  except:
    pris_pr_km = 0.0
  return pris_pr_km


def calc_usage():
  total_km = get_total_km()

  usage = []

  for user in range(4):
    user_km = get_user_km(user)
    user_usage = (user_km / total_km) * 100
    usage.append(int(round(user_usage, 0)))
  return usage


def faq(request):
  return render(request, 'oversigter/faq.html')

