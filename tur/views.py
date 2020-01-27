from django.views.generic import TemplateView
from django.shortcuts import render
from tur.forms import TurForm


class CreateTur(TemplateView):
    template_name = 'tur.html'
    
    def get(self, request):
        form = TurForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TurForm()
        if form.is_valid():
            text = form.cleaned_data['post']
            print(text)
            print('--------------------------------------- her ------------------------------------')
            return redirect('index')

        return render(request, self.template_name, {'form': form})

