from django.shortcuts import render

def show_stats(request):
  return render(request, 'stats.html')