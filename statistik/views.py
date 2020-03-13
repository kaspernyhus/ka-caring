from django.shortcuts import render
from db_functions.db_data import get_total_tankning, get_current_km

def show_stats(request):
  km = get_current_km()
  km = km - 114293 #km ved overtagelse
  tankning = 1
  pris_pr_km = km / tankning

  context = {'pris_pr_km': pris_pr_km}

  return render(request, 'stats.html', context)

def faq(request):
  return render(request, 'faq.html')
