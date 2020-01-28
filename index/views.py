from django.shortcuts import render
from django.http import HttpResponse
from db_functions.db_data import get_current_km

def index(request):
    current_km = get_current_km()
    return render(request, 'index.html', {'current_km': current_km})