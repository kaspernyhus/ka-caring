from django import forms
from datetime import date, datetime, timedelta
from db_functions.users import get_choices


class DateInput(forms.DateInput):
    input_type = 'date'


class BookingForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
      super(BookingForm, self).__init__(*args, **kwargs)
      self.fields['user_id'] = forms.CharField(label='', widget=forms.RadioSelect(choices=get_choices(user), attrs={'class': 'checkbox'}))

    
    start_date = forms.DateField(widget=DateInput(attrs={'class': 'input'}), label='Startdato', initial=datetime.now())
    end_date = forms.DateField(widget=DateInput(attrs={'class': 'input'}), label='Slutdato', initial=datetime.now()+timedelta(1))
    user_id = forms.CharField(label='', widget=forms.RadioSelect(attrs={'class': 'checkbox'}))
    