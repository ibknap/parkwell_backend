from django import forms

class NotifyForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()