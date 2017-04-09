from django import forms
from django.contrib.auth.models import User

#so far the conditionst are very basic, to be strickend
class LoginForm(forms.Form):
  username = forms.CharField(label='Username:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))