from django import forms
from .models import Tankning, Betaling, Udgift
from db_functions.users import get_choices


class DateInput(forms.DateInput):
    input_type = 'date'


class TankningForm(forms.ModelForm):
  def __init__(self, user, *args, **kwargs):
      super(TankningForm, self).__init__(*args, **kwargs)
      self.fields['user_id'] = forms.CharField(label='', widget=forms.RadioSelect(choices=get_choices(user.groups), attrs={'class': 'checkbox'}))
      self.fields['user_id'].initial = user.id

  class Meta:
      model = Tankning
      fields = [
          'date',
          'amount',
          'user_id'
      ]
      widgets = {
          'date': DateInput(attrs={'class': 'input'}),
      }
      labels = {
          'date': 'Dato',
      }
  
  amount = forms.FloatField(label='Beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
  # user_id = forms.CharField(label='', widget=forms.RadioSelect(attrs={'class': 'checkbox'}))


class BetalingForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(BetalingForm, self).__init__(*args, **kwargs)
        self.fields['user_id'] = forms.CharField(label='', widget=forms.RadioSelect(choices=get_choices(user), attrs={'class': 'checkbox'}))

    class Meta:
        model = Betaling
        fields = [
            'date', 
            'amount',
            'user_id'
        ]
        widgets = {
            'date': DateInput(attrs={'class': 'input'}),
        }
        labels = {
            'date': 'Dato',
        }
    
    amount = forms.FloatField(label='Overført beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
    user_id = forms.CharField(label='', widget=forms.RadioSelect(attrs={'class': 'checkbox'}))
    indskud = forms.BooleanField(required=False)


class UdgiftForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UdgiftForm, self).__init__(*args, **kwargs)
        self.fields['user_id'] = forms.CharField(label='', widget=forms.RadioSelect(choices=get_choices(user), attrs={'class': 'checkbox'}))
  
    class Meta:
        model = Udgift
        fields = [
            'date', 
            'amount',
            'description',
            'user_id'
        ]
        widgets = {
            'date': DateInput(attrs={'class': 'input'}),
        }
        labels = {
            'date': 'Dato',
            'user_id': 'Hvem har betalt?'
        }
    
    amount = forms.FloatField(label='Betalt beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
    description = forms.CharField(label='Beskrivelse', widget=forms.Textarea(attrs={'class': 'text-input', 'rows':1, 'cols':30}))
    user_id = forms.CharField(label='Hvem har betalt?', widget=forms.RadioSelect(attrs={'class': 'checkbox'}))


AdminCHOICES=[(8,'Kirsten'),
         (9,'Marie'),
         (7,'Kasper'),
         (10,'Farmor & Farfar'),
         (12,'Bank konto')
        ]

SPLIT=[(0,'Ja'),
        (1,'Nej')
        ]

class AdminUdgiftForm(forms.ModelForm):
    amount = forms.FloatField(label='Betalt beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
    description = forms.CharField(label='Beskrivelse', widget=forms.Textarea(attrs={'class': 'text-input', 'rows':1, 'cols':30}))
    user_id = forms.CharField(label='Hvem har betalt?', widget=forms.RadioSelect(choices=AdminCHOICES, attrs={'class': 'checkbox'}))
    split = forms.CharField(label='Split mellem brugere?', widget=forms.Select(choices=SPLIT))
    
    class Meta:
        model = Udgift
        fields = [
            'date', 
            'amount',
            'description',
            'user_id',
            'split'
        ]
        widgets = {
            'date': DateInput(attrs={'class': 'input'}),
        }
        labels = {
            'date': 'Dato',
            'user_id': 'Hvem har betalt?'
        }