from django.shortcuts import render

def show_stats(request):
  return render(request, 'stats.html')

def faq(request):
  return render(request, 'faq.html')
