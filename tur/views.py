from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from tur.forms import TurForm
from db_functions.db_data import get_username

km_count = 123356

class CreateTur(TemplateView):
    template_name = 'tur.html'
    
    def get(self, request):
        form = TurForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TurForm(request.POST)
        #print(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            km = data['km_count'] - km_count
            print(get_username(data))
            return render(request, 'tur_confirm.html', {'km': km})
            
        else:
            print('------------------------ form not valid ------------------------')
            return render(request, 'form_error.html')
