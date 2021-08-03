from django.db import models
from .models import Booking, Listing
from django import forms

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('created_on', )
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget = forms.TextInput(attrs={'placeholder': 'Your Full Name',})
        self.fields['email'].widget = forms.TextInput(attrs={"placeholder": "Your Email"})
        self.fields['mobile_number'].widget = forms.TextInput(attrs={'placeholder': 'Mobile Number',})
        self.fields['full_name'].label = False
        self.fields['email'].label = False
        self.fields['mobile_number'].label = False

class ContactUsForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(ContactUsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={"placeholder": "Your Name"})
        self.fields['email'].widget = forms.TextInput(attrs={"placeholder": "Your Email"})
        self.fields['subject'].widget = forms.TextInput(attrs={"placeholder": "Subject"})
        self.fields['message'].widget = forms.Textarea(attrs={'row': 4, 'col': 40})
        self.fields['name'].label = False
        self.fields['email'].label = False
        self.fields['subject'].label = False
        self.fields['message'].label = False

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ("park", "created_on")
