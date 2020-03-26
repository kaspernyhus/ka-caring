from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import TankningForm, BetalingForm, UdgiftForm, AdminUdgiftForm
from db_functions.db_data import get_usernames, get_userID, update_user_account, delete_transaction, update_accounts, update_user_saldo, update_bank_account
from emailing.views import udgift_oprettet_mail, tankning_oprettet_mail, indbetaling_oprettet_mail

from django.views.generic.edit import UpdateView
from .models import Tankning, Betaling, Udgift
from datetime import datetime


class CreateTankning(TemplateView):
    template_name = 'tankning.html'
    
    def get(self, request):
        form = TankningForm()
        form.fields['user_id'].initial = get_userID(request.user.username) # auto check current user logged in
        
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

            tankning_oprettet_mail(request.user.username, data)

            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})
        

class CreateBetaling(TemplateView):
    template_name = 'betaling.html'

    def get(self, request):
        form = BetalingForm()
        form.fields['user_id'].initial = get_userID(request.user.username) # auto check current user logged in
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = BetalingForm(request.POST)
        
        if form.is_valid():
            print('----------- indbetaling registreret --------------')
            data = form.cleaned_data
            new_id = update_accounts(request, data, 'Indbetaling')
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.save()

            update_bank_account(new_id, data['amount'], data['user_id'], 'Indbetaling')

            indbetaling_oprettet_mail(request.user.username, data)
            
            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})


class CreateUdgift(TemplateView):
    template_name = 'udgift.html'

    def get(self, request):
        form = UdgiftForm()
        form.fields['user_id'].initial = get_userID(request.user.username) # auto check current user logged in
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UdgiftForm(request.POST)
        
        if form.is_valid():
            print('----------- udgift registreret --------------!!')
            data = form.cleaned_data
            new_id = update_accounts(request, data, 'Udgift')
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.save()
            
            udgift_oprettet_mail(request.user.username, data)

            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})


class CreateAdminUdgift(TemplateView):
    template_name = 'udgift.html'

    def get(self, request):
        form = AdminUdgiftForm()
        form.fields['user_id'].initial = get_userID(request.user.username) # auto check current user logged in
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AdminUdgiftForm(request.POST)
        
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
    form_class = TankningForm
    #fields = ['date', 'amount']
    template_name = 'edit_entries.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        update_user_saldo(instance.transaction_id, instance.user_id, -instance.amount)
        return super(TankningUpdate, self).form_valid(form)


class BetalingUpdate(UpdateView):
    model = Betaling
    form_class = BetalingForm
    #fields = ['date', 'amount']
    template_name = 'edit_entries.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        update_user_saldo(instance.transaction_id, instance.user_id, -instance.amount)
        return super(BetalingUpdate, self).form_valid(form)


class UdgiftUpdate(UpdateView):
    model = Udgift
    form_class = UdgiftForm
    #fields = ['date', 'amount', 'description', 'user_id']
    template_name = 'edit_entries.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        update_user_saldo(instance.transaction_id, instance.user_id, instance.amount)
        return super(UdgiftUpdate, self).form_valid(form)


class CreateUdbetaling(TemplateView):
    template_name = 'udbetaling.html'

    def get(self, request):
        form = BetalingForm()
        form.fields['user_id'].initial = get_userID(request.user.username) # auto check current user logged in
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = BetalingForm(request.POST)
        
        if form.is_valid():
            print('----------- Udbetaling registreret --------------')
            data = form.cleaned_data
            data['amount'] = -data['amount']
            new_id = update_accounts(request, data, 'Udbetaling')
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.amount = data['amount']
            save_with_id.save()

            update_bank_account(new_id, data['amount'], data['user_id'], 'Udbetaling')
            
            return render(request, 'betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'user': get_usernames(data['user_id'])})
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
            return render(request, 'form_error.html', {'error': 'Husk at vælge en brugere'})