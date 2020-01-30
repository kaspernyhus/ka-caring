from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import TurForm
from db_functions.db_data import get_usernames, get_current_km, update_account


class CreateTur(TemplateView):
    template_name = 'tur.html'
    
    def get(self, request):
        data = {'km_count': get_current_km()}
        form = TurForm(initial=data)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TurForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            previous_km_count = get_current_km()
            
            if data['km_count'] > previous_km_count:
                form_obj = form.save(commit=False)

                km = data['km_count'] - previous_km_count
                tur_pris = km * 2.0

                form_obj.delta_km = km
                form_obj.price = tur_pris
                form_obj.save()

                update_account(data['user_id'], tur_pris, km)
                return render(request, 'tur_confirm.html', {'km': km, 'tur_pris': tur_pris, 'users': get_usernames(data['user_id'])})
            
            else:
                return render(request, 'form_error.html', {'error': 'Nuværende kilometertælleraflæsning skal være højere end den seneste!'})
            
        else:
            print('------------------------ form not valid ------------------------')
            return render(request, 'form_error.html', {'error': 'Husk at vælge en eller flere brugere'})
