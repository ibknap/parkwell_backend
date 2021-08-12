from .models import Booking, Waitlist
from django import forms

class WaitlistForm(forms.ModelForm):
    class Meta:
        model = Waitlist
        exclude = ('created_on', )
    def __init__(self, *args, **kwargs):
        super(WaitlistForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={"placeholder": "Your Email Address"})
        self.fields['email'].label = False

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
