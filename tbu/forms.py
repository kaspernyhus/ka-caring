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
            'date': DateInput(),
        }
    amount = forms.FloatField(label='Beløb:', widget=forms.NumberInput(attrs={'type':'number', 'pattern': "\d*"}))
    user_id = forms.CharField(label='', initial='0', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'checkbox'}))


class BetalingForm(forms.ModelForm):
    amount = forms.FloatField(label='Overført beløb:', widget=forms.NumberInput(attrs={'type':'number', 'pattern': "\d*"}))
    user_id = forms.CharField(label='', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'checkbox'}))
    
    class Meta:
        model = Betaling
        fields = [
            'date', 
            'amount',
            'user_id'
        ]
        widgets = {
            'date': DateInput(),
        }


class UdgiftForm(forms.ModelForm):
    amount = forms.FloatField(label='Betalt beløb:', widget=forms.NumberInput(attrs={'type':'number', 'pattern': "\d*"}))
    description = forms.CharField(label='Beskrivelse', widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    user_id = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(choices=CHOICES, attrs={'class': 'checkbox'}))
    class Meta:
        model = Udgift
        fields = [
            'date', 
            'amount',
            'description',
            'user_id'
        ]
        widgets = {
            'date': DateInput(),
        }