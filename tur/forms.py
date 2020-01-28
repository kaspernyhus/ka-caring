from django import forms
from .models import Ture

current_km = 123456

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
    km_count = forms.IntegerField(label='Kilometertæller', initial=current_km, widget=forms.NumberInput(attrs={'pattern': "\d*"}))
    user_id = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(choices=CHOICES, attrs={'class': 'checkbox'}))
    ekstra = forms.CharField(label='Ekstra passager', widget=forms.Select(choices=EKSTRA))
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
    

