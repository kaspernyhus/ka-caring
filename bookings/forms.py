from django import forms
from datetime import date, datetime, timedelta


CHOICES=[(0,'Kirsten'),
         (1,'Marie'),
         (2,'Kasper'),
         (3,'Farmor & Farfar')
        ]


class DateInput(forms.DateInput):
    input_type = 'date'


class BookingForm(forms.Form):
    start_date = forms.DateField(widget=DateInput(attrs={'class': 'input'}), label='Startdato', initial=datetime.now())
    end_date = forms.DateField(widget=DateInput(attrs={'class': 'input'}), label='Slutdato', initial=datetime.now()+timedelta(1))
    user_id = forms.CharField(label='', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'checkbox'}))
    