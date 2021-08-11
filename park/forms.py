from django.http import request
from account.models import ParkAdmin
from .models import Park
from django import forms

class ParkForm(forms.ModelForm):
    class Meta:
        model = Park
        exclude = ('company', 'created_on' )
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super (ParkForm,self ).__init__(*args,**kwargs)
        if self.request.user.is_authenticated:
            try:
                self.fields['park_admin'].queryset = ParkAdmin.objects.filter(company_admin=self.request.user.administrator)
            except:
                pass