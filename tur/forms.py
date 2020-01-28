from django import forms
from .models import Ture

current_km = 123456

CHOICES=[(0,'Marie'),
         (1,'Kirsten'),
         (2,'Kasper'),
         (3,'Ved Ikke'),
        ]


class DateInput(forms.DateInput):
    input_type = 'date'


class TurForm(forms.ModelForm):
    km_count = forms.IntegerField(label='Kilometertæller', initial=current_km, widget=forms.NumberInput(attrs={'pattern': "\d*"}))
    user_id = forms.CharField(label='Bruger', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'radioselect'}))
    class Meta:
        model = Ture
        fields = [
            'dato', 
            'km_count', 
            'user_id'
        ]
        widgets = {
            'dato': DateInput(),
        }
    

