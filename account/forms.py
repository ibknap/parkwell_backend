from account.models import Administrator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=250, required='required', widget=forms.TextInput(attrs={'placeholder': 'choose username',}))
    email = forms.EmailField(max_length=250, required='required', widget=forms.EmailInput(attrs={'placeholder': 'active email address',}))
    password1 = forms.CharField(max_length=250, required='required', widget=forms.PasswordInput(attrs={'placeholder': 'choose password',}))
    password2 = forms.CharField(max_length=250, required='required', widget=forms.PasswordInput(attrs={'placeholder': 'confirm password',}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required='required', widget=forms.TextInput(attrs={'placeholder': 'your username',}))
    password = forms.CharField(max_length=250, required='required', widget=forms.PasswordInput(attrs={'placeholder': 'your password',}))
    
    class Meta:
        model = User
        fields = ('username', 'password' )

class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ('mobile_number', )
    def __init__(self, *args, **kwargs):
        super(AdministratorForm, self).__init__(*args, **kwargs)
        self.fields['mobile_number'].widget = forms.TextInput(attrs={'placeholder': 'mobile number',})
        self.fields['mobile_number'].label = False

class UpdateFirstNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',)
    def __init__(self, *args, **kwargs):
        super(UpdateFirstNameForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'first name',})
        self.fields['first_name'].label = False

class UpdateLastNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name',)
    def __init__(self, *args, **kwargs):
        super(UpdateLastNameForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'last name',})
        self.fields['last_name'].label = False