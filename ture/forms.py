from django import forms
from .models import Ture
from db_functions.transactions import get_current_km
from db_functions.users import get_choices


# CHOICES=[(8,'Kirsten'),
#          (9,'Marie'),
#          (7,'Kasper'),
#          (10,'Farmor & Farfar'),
#          (4,'Tur mangler')
#         ]

EKSTRA=[(0,''),
        (1,'Kirsten +1'),
        (2,'Marie +1'),
        (3,'Kasper +1'),
        (4,'Farmor & Farfar +1'),
        (5,'Kirsten +2'),
        (6,'Marie +2'),
        (7,'Kasper +2'),
        (8,'Farmor & Farfar +2')
        ]


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
    #user_id = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(choices=get_choices(tur=True), attrs={'class': 'checkbox'}))

