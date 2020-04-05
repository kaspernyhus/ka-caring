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
  

class BetalingForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(BetalingForm, self).__init__(*args, **kwargs)
        self.fields['user_id'] = forms.CharField(label='', widget=forms.RadioSelect(choices=get_choices(user.groups), attrs={'class': 'checkbox'}))
        self.fields['user_id'].initial = user.id

        if user.groups.filter(name='VIP').exists() or user.groups.filter(name='ALL').exists():
            self.fields['is_indskud'] = forms.BooleanField(label='Indskud:', required=False)

    class Meta:
        model = Betaling
        fields = [
            'date', 
            'amount',
            'user_id',
        ]
        widgets = {
            'date': DateInput(attrs={'class': 'input'}),
        }
        labels = {
            'date': 'Dato',
        }
    
    amount = forms.FloatField(label='Overført beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
    

class UdbetalingForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UdbetalingForm, self).__init__(*args, **kwargs)
        self.fields['user_id'] = forms.CharField(label='Hvem skal beløbet udbetales til?', widget=forms.RadioSelect(choices=get_choices(user.groups), attrs={'class': 'checkbox'}))
        

    class Meta:
        model = Betaling
        fields = [
            'date', 
            'amount',
            'user_id',
        ]
        widgets = {
            'date': DateInput(attrs={'class': 'input'}),
        }
        labels = {
            'date': 'Dato',
        }
    
    amount = forms.FloatField(label='Overført beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
    


class UdgiftForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UdgiftForm, self).__init__(*args, **kwargs)
        
        CHOICES = get_choices(user.groups)
        if user.groups.filter(name='ALL').exists():
            CHOICES.append((0,'Fælles-konto'))

        self.fields['user_id'] = forms.CharField(label='', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'checkbox'}))
        self.fields['user_id'].initial = user.id

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
    