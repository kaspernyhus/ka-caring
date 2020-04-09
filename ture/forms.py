from django import forms
from .models import Ture
from db_functions.transactions import get_current_km
from db_functions.users import get_choices, EKSTRA


class DateInput(forms.DateInput):
    input_type = 'date'


class TurForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
      super(TurForm, self).__init__(*args, **kwargs)
      self.fields['user_id'] = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(choices=get_choices(user.groups, tur=True), attrs={'class': 'checkbox'}))
      self.fields['user_id'].initial = user.id
      self.fields['km_count'].initial = get_current_km()
    
    class Meta:
        model = Ture
        fields = [
            'date', 
            'km_count', 
            'user_id',
            'extra_pas'
        ]
        widgets = {
            'date': DateInput(attrs={'class': 'input'}),
        }
        labels = {
            'date': 'Dato'
        }
    
    current_km = get_current_km()
    km_count = forms.IntegerField(label='Kilometertæller', initial=current_km, widget=forms.NumberInput(attrs={'class': 'input', 'pattern': "\d*"}))
    extra_pas = forms.CharField(label='Ekstra passager', widget=forms.Select(choices=EKSTRA))


class TurUpdateForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TurUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user_id'] = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(choices=get_choices(user.groups, tur=True), attrs={'class': 'checkbox'}))    
        
    class Meta:
        model = Ture
        fields = [
            'date', 
            'user_id',
            'extra_pas',
        ]
        widgets = {
            'date': DateInput(attrs={'class': 'input'}),
        }
        labels = {
            'date': 'Dato'
        }
    
    extra_pas = forms.CharField(label='Ekstra passager', widget=forms.Select(choices=EKSTRA))