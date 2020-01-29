from django import forms
from .models import Ture
from db_functions.db_data import get_current_km


CHOICES=[(0,'Kirsten'),
         (1,'Marie'),
         (2,'Kasper'),
         (3,'Tur mangler')
        ]

EKSTRA=[(0,''),
        (1,'Kirsten +1'),
        (2,'Marie +1'),
        (3,'Kasper +1'),
        (4,'Kirsten +2'),
        (5,'Marie +2'),
        (6,'Kasper +2')
        ]


class DateInput(forms.DateInput):
    input_type = 'date'


class TurForm(forms.ModelForm):
    current_km = get_current_km()
    
    km_count = forms.IntegerField(label='Kilometertæller', initial=current_km, widget=forms.NumberInput(attrs={'pattern': "\d*"}))
    user_id = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(choices=CHOICES, attrs={'class': 'checkbox'}))
    extra_pas = forms.CharField(label='Ekstra passager', widget=forms.Select(choices=EKSTRA))
    class Meta:
        model = Ture
        fields = [
            'dato', 
            'km_count', 
            'user_id',
            'extra_pas'
        ]
        widgets = {
            'dato': DateInput(),
        }
    

