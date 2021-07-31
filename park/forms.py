from .models import Park
from django import forms

class ParkForm(forms.ModelForm):
    class Meta:
        model = Park
        exclude = ('company', 'created_on' )