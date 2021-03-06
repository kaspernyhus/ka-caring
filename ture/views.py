from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import TurForm, TurUpdateForm
from kacaring.km_price import get_km_price
from db_functions.transactions import create_new_transaction, get_current_km, update_accounts, update_user_km
from db_functions.users import get_usernames, extra_pas
from emailing.views import add_to_mail_Q
from django.views.generic.edit import UpdateView
from .models import Ture
from accounts.models import TransactionId



class CreateTur(TemplateView):
    template_name = 'transactions/tur.html'
    
    def get(self, request):
        form = TurForm(request.user)
        return render(request, self.template_name, {'form': form, 'km_price': get_km_price(request.user.groups)})
    
    def post(self, request):
        form = TurForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            new_id = create_new_transaction(request, 'Tur')
            
            previous_km_count = get_current_km()
            
            if data['km_count'] > previous_km_count:
                form_obj = form.save(commit=False)
                form_obj.transaction_id = new_id

                km = data['km_count'] - previous_km_count
                tur_pris = km * get_km_price(request.user.groups)

                form_obj.delta_km = km
                form_obj.price = tur_pris
                
                data.update({'amount': tur_pris})
                
                print(data)
                update_accounts(request, new_id, data, 'Tur', km=km)
   
                form_obj.save()
                
                add_to_mail_Q(request.user.username, data, 'Tur')

                context = {'km': km, 'tur_pris': tur_pris, 'users': get_usernames(eval(data['user_id'])), 'extra_pas': extra_pas(data)[1]}
                return render(request, 'transactions/tur_confirm.html', context)
            
            else:
                return render(request, 'transactions/form_error.html', {'error': 'Nuværende kilometertælleraflæsning skal være højere end den seneste!'})
        else:
            return render(request, 'transactions/form_error.html', {'error': 'Husk at vælge en eller flere brugere'})


class TurUpdate(UpdateView):
    model = Ture
    form_class = TurUpdateForm
    template_name = 'transactions/edit_entries.html'
    success_url = '/oversigt/alle_transaktioner' 

    def get_form_kwargs(self):
        kwargs = super(TurUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data

        form_obj = form.save(commit=False)

        db_data = Ture.objects.get(id=form_obj.id)
        transaction_id = db_data.transaction_id
        
        #Delete
        old_transaction = TransactionId.objects.get(transaction_id=transaction_id)
        old_transaction.delete()

        #Create new transaction
        new_id = create_new_transaction(self.request, 'Tur')
        
        data.update({'amount': db_data.price})
        
        update_accounts(self.request, new_id, data, 'Tur', km=db_data.delta_km)

        form_obj.save()

        return super(TurUpdate, self).form_valid(form)