from django import forms
from .models import Ture

class TurForm(forms.ModelForm):
    class Meta:
        model = Ture
        fields = ['dato', 'km', 'user_id']
    

