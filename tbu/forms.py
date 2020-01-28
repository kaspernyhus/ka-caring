from django import forms
from .models import Tankning

CHOICES=[(0,'Marie'),
         (1,'Kirsten'),
         (2,'Kasper'),
         (3,'Gæst'),
         (4,'Ved Ikke')
        ]


class DateInput(forms.DateInput):
    input_type = 'date'


class TankningForm(forms.ModelForm):
    pris = forms.FloatField(label='Pris:', widget=forms.NumberInput(attrs={'pattern': "\d*"}))
    user_id = forms.CharField(label='', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'radioselect'}))
    class Meta:
        model = Tankning
        fields = [
            'dato', 
            'pris', 
            'user_id'
        ]
        widgets = {
            'dato': DateInput(),
        }
    

