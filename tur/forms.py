from django import forms
from .models import Tur

class TurForm(forms.ModelForm):
    class Meta:
        model = Tur
        fields = ['km', 'user_id']
    

