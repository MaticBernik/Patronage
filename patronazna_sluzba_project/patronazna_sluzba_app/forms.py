from django import forms
from django.contrib.auth.models import User
from .models import Pacient
from django.core.validators import MaxValueValidator


#so far the conditionst are very basic, to be strickend
class LoginForm(forms.Form):
  username = forms.CharField(label='Username:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  
SEX_CHOICES = (
    ('1', 'Moski'),
    ('2', 'Zenski'),
)
DISTRICT_CHOICES = (
	('1', ''),
    ('2', '05600 - VIC-RUDNIK'),
    ('3', '05470 - SISKA'),
	('4', '05030 - BEZIGRAD'),
    ('5', '05300 - MOSTE-POLJE'),
)

RELATIONS = (
	('1', 'STARS'),
    ('2', 'OTROK'),
    ('3', 'VNUK'),
	('4', 'STARI STARSI'),
)

class RegistrationFrom(forms.Form):
   cardNumber = forms.IntegerField(label='Stevilka kartice:', widget=forms.NumberInput(attrs={'class': 'form-control'}))
   surname = forms.CharField(label='Priimek:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   name = forms.CharField(label='Ime:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   address = forms.CharField(label='Naslov:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   phone = forms.IntegerField(label='Telefon:', widget=forms.TextInput(attrs={'class': 'form-control'}))
   password = forms.CharField(label='Geslo',max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   password2 = forms.CharField(label='Ponovi geslo',max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   sex = forms.ChoiceField(choices=SEX_CHOICES)
   district = forms.ChoiceField(choices=DISTRICT_CHOICES)
   email = forms.EmailField()
   
   contact_surname = forms.CharField(label='Priimek:',  required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   contact_name = forms.CharField(label='Ime:',  required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   contact_address = forms.CharField(label='Naslov:', required=False,  max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   contact_phone_number = forms.IntegerField(label='Telefon',  required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
   contact_sorodstvo = forms.CharField(label='Sorodstvo:',  required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   birthDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}), input_formats=['%d-%m-%Y'])
   postCode =  forms.CharField(label='Posta', max_length=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))

class AddNursingPatient(forms.Form):
	cardNumber = forms.IntegerField(label='Stevilka kartice:', widget=forms.NumberInput(attrs={'class': 'form-control'}))
	surname = forms.CharField(label='Priimek:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	name = forms.CharField(label='Ime:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	address = forms.CharField(label='Naslov:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	phone = forms.IntegerField(label='Telefon:',  widget=forms.NumberInput(attrs={'class': 'form-control'}))
	birthDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}), input_formats=['%d-%m-%Y'])
	postCode =  forms.CharField(label='Posta', max_length=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	sex = forms.ChoiceField(choices=SEX_CHOICES)
	district = forms.ChoiceField(choices=DISTRICT_CHOICES)
	relation = forms.ChoiceField(label='Sorodstvo:', choices = RELATIONS )