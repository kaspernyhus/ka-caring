from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import TurForm
from kacaring.km_price import get_km_price
from db_functions.db_data import get_usernames, get_userID, get_current_km, update_user_account, update_accounts, update_user_saldo, update_user_km, extra_pas

from django.views.generic.edit import UpdateView
from .models import Ture


class CreateTur(TemplateView):
    template_name = 'tur.html'
    
    def get(self, request):
        data = {'km_count': get_current_km()}
        form = TurForm(initial=data)
        form.fields['user_id'].initial = get_userID(request.user.username) # auto check current user logged in
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TurForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            previous_km_count = get_current_km()
            
            if data['km_count'] > previous_km_count:
                form_obj = form.save(commit=False)

                km = data['km_count'] - previous_km_count
                tur_pris = km * get_km_price()

                form_obj.delta_km = km
                form_obj.price = tur_pris
                
                data.update({'amount': tur_pris})
                new_id = update_accounts(request, data, 'Tur', km=km)

                form_obj.transaction_id = new_id                
                form_obj.save()
                
                context = {'km': km, 'tur_pris': tur_pris, 'users': get_usernames(data['user_id']), 'extra_pas': extra_pas(data)[1]}

                return render(request, 'tur_confirm.html', context)
            
            else:
                return render(request, 'form_error.html', {'error': 'Nuværende kilometertælleraflæsning skal være højere end den seneste!'})
            
        else:
            print('------------------------ form not valid ------------------------')
            return render(request, 'form_error.html', {'error': 'Husk at vælge en eller flere brugere'})


class TurUpdate(UpdateView):
    model = Ture
    fields = ['date', 'km_count', 'user_id', 'extra_pas']
    template_name = 'edit_entries.html'
    success_url = '/'
    
    def form_valid(self, form):
        form_obj = form.save(commit=False)
        
        # recalc other tur data
        data = Ture.objects.get(id=form_obj.id)
        new_delta_km = data.delta_km + form_obj.km_count - data.km_count
        form_obj.delta_km = new_delta_km
        tur_pris = new_delta_km * get_km_price()
        form_obj.price = tur_pris

        form_obj.user = self.request.user
        print(form_obj.user)

        try:
            update_user_km(form_obj.transaction_id, form_obj.user_id, form_obj.delta_km, form_obj.price)
        except:
            data = form.cleaned_data
            data.update({'amount': tur_pris})

            new_id = update_accounts(self.request, data, 'Tur', km=new_delta_km)
            
            form_obj.transaction_id = new_id                
            form_obj.save()

        return super(TurUpdate, self).form_valid(form)