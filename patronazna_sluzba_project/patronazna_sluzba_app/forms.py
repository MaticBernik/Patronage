from django import forms
from django.contrib.auth.models import User
from .models import Pacient

#so far the conditionst are very basic, to be strickend
class LoginForm(forms.Form):
  username = forms.CharField(label='Username:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  

class RegistrationFrom(forms.Form):
   cardNumber = forms.CharField(label='Številka kartice:', max_length=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))
   surname = forms.CharField(label='Priimek:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   name = forms.CharField(label='Ime:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   address = forms.CharField(label='Naslov:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   phone = forms.CharField(label='Telefon:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   password = forms.CharField(label='Geslo',max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   password2 = forms.CharField(label='Ponovi geslo',max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   birthDate = forms.DateField()
   