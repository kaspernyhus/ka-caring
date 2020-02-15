from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import TankningForm, BetalingForm, UdgiftForm
from db_functions.db_data import get_usernames, get_userID, update_user_account, delete_transaction, update_accounts

from django.views.generic.edit import UpdateView
from .models import Tankning, Betaling, Udgift


class CreateTankning(TemplateView):
    template_name = 'tankning.html'
    
    def get(self, request):
        form = TankningForm()
        form.fields['user_id'].initial = get_userID(request.user) # auto check current user logged in
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TankningForm(request.POST)
        
        if form.is_valid():
            print('----------- tankning registreret --------------')
            data = form.cleaned_data
            new_id = update_accounts(request, data, 'Tankning')
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.save()

            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})
        

class CreateBetaling(TemplateView):
    template_name = 'betaling.html'

    def get(self, request):
        form = BetalingForm()
        form.fields['user_id'].initial = get_userID(request.user) # auto check current user logged in
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = BetalingForm(request.POST)
        
        if form.is_valid():
            print('----------- betaling registreret --------------')
            data = form.cleaned_data
            new_id = update_accounts(request, data, 'Betaling')
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.save()
            
            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})


class CreateUdgift(TemplateView):
    template_name = 'udgift.html'

    def get(self, request):
        form = UdgiftForm()
        form.fields['user_id'].initial = get_userID(request.user) # auto check current user logged in
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UdgiftForm(request.POST)
        
        if form.is_valid():
            print('----------- udgift registreret --------------')
            data = form.cleaned_data
            new_id = update_accounts(request, data, 'Udgift')
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.save()
            
            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})


class TankningUpdate(UpdateView):
    model = Tankning
    fields = ['date', 'amount']
    template_name = 'edit_entries.html'
    success_url = '/'


class BetalingUpdate(UpdateView):
    model = Betaling
    fields = ['date', 'amount']
    template_name = 'edit_entries.html'
    success_url = '/'