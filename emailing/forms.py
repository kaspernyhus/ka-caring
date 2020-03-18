from django import forms
from .models import UserPreferences

CHOICES=[(0,'Månedlig konto-oversigt'),
         (1,'Udgift oprettet'),
         (2,'Tankning oprettet'),
         (3,'Tur oprettet')
        ]


class UserPrefForm(forms.ModelForm):
  class Meta:
        model = UserPreferences
        fields = [
            
        ]
  
  user_prefs = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(choices=CHOICES, attrs={'class': 'checkbox'}))