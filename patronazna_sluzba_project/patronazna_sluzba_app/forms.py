from django import forms
from django.contrib.auth.models import User

#so far the conditionst are very basic, to be strickend
class LoginForm(forms.Form):
  username = forms.CharField(label='Username:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterMedicalStaffForm(forms.Form):
# check medical_id length, same for medical_area_id and phone_number_id
  medical_id = forms.IntegerField(label="medical_personal_id", widget=forms.NumberInput(attrs={'class': 'form-control'}))
  name = forms.CharField(label='med_name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  surname = forms.CharField(label='med_surname', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  medical_area_id = forms.IntegerField(label="medical_area_id", widget=forms.NumberInput(attrs={'class': 'form-control'}))
  email = forms.EmailField(label="email", max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
  phone_number = forms.IntegerField(label="phone_number", widget=forms.NumberInput(attrs={'class': 'form-control'}))
  password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  USER_TYPES = (('doc', 'Zdravnik'), 
  				('nurse', 'Medicinska sestra/brat'),
  				('head_of_medical_service', 'Vodja patronazne sluzbe'),
  				('employee', 'Usluzbenec zdravstvene ustanove')
  	)
  role = forms.ChoiceField(choices=USER_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))