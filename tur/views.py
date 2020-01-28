from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from tur.forms import TurForm


class CreateTur(TemplateView):
    template_name = 'tur.html'
    
    def get(self, request):
        form = TurForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TurForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('------------------------ form not valid ------------------------')
            print(form.errors)
        return redirect('index')

