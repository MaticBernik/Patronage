from django import forms
from django.contrib.auth.models import User
from .models import Pacient

#so far the conditionst are very basic, to be strickend
class LoginForm(forms.Form):
  username = forms.CharField(label='Username:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  
SEX_CHOICES = (
    ('1', 'Moški'),
    ('2', 'Ženski'),
)
DISTRICT_CHOICES = (
	('1', ''),
    ('2', '05600 - VIČ-RUDNIK'),
    ('3', '05470 - ŠIŠKA'),
	('4', '05030 - BEŽIGRAD'),
    ('5', '05300 - MOSTE-POLJE'),
)
class RegistrationFrom(forms.Form):
   cardNumber = forms.CharField(label='Številka kartice:', max_length=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))
   surname = forms.CharField(label='Priimek:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   name = forms.CharField(label='Ime:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   address = forms.CharField(label='Naslov:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   phone = forms.CharField(label='Telefon:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   password = forms.CharField(label='Geslo',max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   password2 = forms.CharField(label='Ponovi geslo',max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   sex = forms.ChoiceField(choices=SEX_CHOICES)
   district = forms.ChoiceField(choices=DISTRICT_CHOICES)
   email = forms.EmailField()
   
   contact_surname = forms.CharField(label='Priimek:',  required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   contact_name = forms.CharField(label='Ime:',  required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   contact_address = forms.CharField(label='Naslov:', required=False,  max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   contact_phone_number = forms.CharField(label='Telefon',  required=False,  max_length=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))
   contact_sorodstvo = forms.CharField(label='Sorodstvo:',  required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   birthDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
   postCode =  forms.CharField(label='Pošta', max_length=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))