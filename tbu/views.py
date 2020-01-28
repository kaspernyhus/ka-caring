from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import TankningForm


class CreateTankning(TemplateView):
    template_name = 'tankning.html'
    
    def get(self, request):
        form = TankningForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TankningForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
        return redirect('index')

