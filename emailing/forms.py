from django import forms
from .models import EmailPreferences


def get_choices(user_groups):
  if user_groups.filter(name='VIP').exists() or user_groups.filter(name='ALL').exists():
    CHOICES=[(0,'Månedlig konto-oversigt'),
            (1,'Udgift oprettet'),
            (2,'Tankning oprettet'),
            (3,'Tur oprettet')
            ]
  else:
    CHOICES=[(0,'Månedlig konto-oversigt'),
            ]

  return CHOICES


class UserPrefForm(forms.ModelForm):
  def __init__(self, user, *args, **kwargs):
        super(UserPrefForm, self).__init__(*args, **kwargs)
        self.fields['user_prefs'] = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(choices=get_choices(user.groups), attrs={'class': 'checkbox'}))

  user_prefs = forms.CharField(label='', widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}))
  
  class Meta:
        model = EmailPreferences
        fields = [
            
        ]