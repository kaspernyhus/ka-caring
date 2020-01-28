from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from tur.forms import TurForm
from db_functions.db_data import get_usernames, get_current_km


class CreateTur(TemplateView):
    template_name = 'tur.html'
    
    def get(self, request):
        form = TurForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TurForm(request.POST)
        #print(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            previous_km_count = get_current_km()
            
            if data['km_count'] > previous_km_count:
                form.save()

                km = data['km_count'] - previous_km_count
                return render(request, 'tur_confirm.html', {'km': km, 'users': get_usernames(data)})
            else:
                return render(request, 'form_error.html', {'error': 'Nuværende kilometertælleraflæsning skal være højere end den seneste!'})
            
        else:
            print('------------------------ form not valid ------------------------')
            return render(request, 'form_error.html', {'error': 'Husk at vælge en eller flere brugere'})
