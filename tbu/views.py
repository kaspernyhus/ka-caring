from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import TankningForm, BetalingForm, UdgiftForm, UdbetalingForm
from db_functions.users import get_usernames
from db_functions.transactions import create_new_transaction, update_accounts, update_user_saldo
from emailing.views import add_to_mail_Q
from django.views.generic.edit import UpdateView
from .models import Tankning, Betaling, Udgift
from datetime import datetime


###############################
#     create transactions     #
###############################

class CreateTankning(TemplateView):
    template_name = 'transactions/tankning.html'
    
    def get(self, request):
        form = TankningForm(request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TankningForm(request.user, request.POST)
        if form.is_valid():
            new_id = create_new_transaction(request, 'Tankning')
            data = form.cleaned_data
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.save()

            update_accounts(request, new_id, data, 'Tankning')

            add_to_mail_Q(request.user.username, data, 'Tankning')

            return render(request, 'transactions/betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'users': get_usernames(data['user_id'])})
        else:
            return render(request, 'transactions/form_error.html', {'error': 'Husk at vælge en brugere'})
        

class CreateBetaling(TemplateView):
    template_name = 'transactions/betaling.html'

    def get(self, request):
        form = BetalingForm(request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = BetalingForm(request.user, request.POST)
        
        if form.is_valid():
            new_id = create_new_transaction(request, 'Betaling')
            data = form.cleaned_data

            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.is_indskud = data['is_indskud']
            save_with_id.save()

            if data['is_indskud']:
              update_accounts(request, new_id, data, 'Indskud')
            else:
              update_accounts(request, new_id, data, 'Indbetaling')

            add_to_mail_Q(request.user.username, data, 'Indbetaling')
            
            return render(request, 'transactions/betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'users': get_usernames(data['user_id'])})
        else:
            return render(request, 'transactions/form_error.html', {'error': 'Husk at vælge en brugere'})


class CreateUdgift(TemplateView):
    template_name = 'transactions/udgift.html'

    def get(self, request):
        form = UdgiftForm(request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UdgiftForm(request.user, request.POST)
        
        if form.is_valid():
            new_id = create_new_transaction(request, 'Udgift')
            data = form.cleaned_data
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.save()
            
            update_accounts(request, new_id, data, 'Udgift')
            
            add_to_mail_Q(request.user.username, data, 'Udgift')

            return render(request, 'transactions/betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'users': get_usernames(data['user_id'])})
        else:
            return render(request, 'transactions/form_error.html', {'error': 'Husk at vælge en brugere'})


class CreateUdbetaling(TemplateView):
    template_name = 'transactions/udbetaling.html'

    def get(self, request):
        form = UdbetalingForm(request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UdbetalingForm(request.user, request.POST)
        
        if form.is_valid():
            new_id = create_new_transaction(request, 'Udbetaling')
            data = form.cleaned_data
            
            save_with_id = form.save(commit=False)
            save_with_id.transaction_id = new_id
            save_with_id.amount = -data['amount']
            save_with_id.is_indskud = 0
            save_with_id.save()
            
            update_accounts(request, new_id, data, 'Udbetaling')
            
            return render(request, 'transactions/betaling_confirm.html', {'date': data['date'], 'amount': data['amount'], 'users': get_usernames(data['user_id'])})
        else:
            return render(request, 'transactions/form_error.html', {'error': 'Husk at vælge en brugere'})



###############################
#     update transactions     #
###############################

class TankningUpdate(UpdateView):
    model = Tankning
    form_class = TankningForm
    template_name = 'transactions/edit_entries.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        update_user_saldo(instance.transaction_id, instance.user_id, -instance.amount)
        return super(TankningUpdate, self).form_valid(form)


class BetalingUpdate(UpdateView):
    model = Betaling
    form_class = BetalingForm
    #fields = ['date', 'amount']
    template_name = 'transactions/edit_entries.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        update_user_saldo(instance.transaction_id, instance.user_id, -instance.amount)
        return super(BetalingUpdate, self).form_valid(form)


class UdgiftUpdate(UpdateView):
    model = Udgift
    form_class = UdgiftForm
    #fields = ['date', 'amount', 'description', 'user_id']
    template_name = 'transactions/edit_entries.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        update_user_saldo(instance.transaction_id, instance.user_id, instance.amount)
        return super(UdgiftUpdate, self).form_valid(form)