from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import TankningForm, BetalingForm, UdgiftForm
from db_functions.db_data import get_usernames


class CreateTankning(TemplateView):
    template_name = 'tankning.html'
    
    def get(self, request):
        form = TankningForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TankningForm(request.POST)
        
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            print(data)
            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})
        

class CreateBetaling(TemplateView):
    template_name = 'betaling.html'

    def get(self, request):
        form = BetalingForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = BetalingForm(request.POST)
        
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})


class CreateUdgift(TemplateView):
    template_name = 'udgift.html'

    def get(self, request):
        form = UdgiftForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UdgiftForm(request.POST)
        
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})