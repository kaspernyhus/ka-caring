from django import forms
from .models import Tankning, Betaling, Udgift


CHOICES=[(0,'Kirsten'),
         (1,'Marie'),
         (2,'Kasper'),
         (3,'Farmor & Farfar')
        ]


class DateInput(forms.DateInput):
    input_type = 'date'


class TankningForm(forms.ModelForm):
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
    user_id = forms.CharField(label='', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'checkbox'}))


class BetalingForm(forms.ModelForm):
    amount = forms.FloatField(label='Overført beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
    user_id = forms.CharField(label='', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'checkbox'}))
    
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


class UdgiftForm(forms.ModelForm):
    amount = forms.FloatField(label='Betalt beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
    description = forms.CharField(label='Beskrivelse', widget=forms.Textarea(attrs={'class': 'text-input', 'rows':1, 'cols':30}))
    user_id = forms.CharField(label='Hvem har betalt?', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'checkbox'}))
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


AdminCHOICES=[(0,'Kirsten'),
         (1,'Marie'),
         (2,'Kasper'),
         (3,'Farmor & Farfar'),
         (4,'Bank konto')
        ]


class AdminUdgiftForm(forms.ModelForm):
    amount = forms.FloatField(label='Betalt beløb:', widget=forms.NumberInput(attrs={'class': 'input', 'type':'number', 'pattern': "\d*"}))
    description = forms.CharField(label='Beskrivelse', widget=forms.Textarea(attrs={'class': 'text-input', 'rows':1, 'cols':30}))
    user_id = forms.CharField(label='Hvem har betalt?', widget=forms.RadioSelect(choices=AdminCHOICES, attrs={'class': 'checkbox'}))
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