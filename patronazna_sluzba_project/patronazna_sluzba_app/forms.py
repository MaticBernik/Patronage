from django import forms
from django.contrib.auth.models import User
from .models import *
from django.core.validators import MaxValueValidator


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
  password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  USER_TYPES = (('doc', 'Zdravnik'), 
  				('nurse', 'Medicinska sestra/brat'),
  				('head_of_medical_service', 'Vodja patronazne sluzbe'),
  				('employee', 'Usluzbenec zdravstvene ustanove')
  	)
  role = forms.ChoiceField(choices=USER_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))

SEX_CHOICES = (
    ('1', 'Moski'),
    ('2', 'Zenski'),
)
DISTRICT_CHOICES = (
    ('1', '05600 - VIC-RUDNIK'),
    ('2', '05470 - SISKA'),
	('3', '05030 - BEZIGRAD'),
    ('4', '05300 - MOSTE-POLJE'),
)

RELATIONS = (
	('1', 'STARS'),
    ('2', 'OTROK'),
    ('3', 'VNUK'),
	('4', 'STARI STARSI'),
)
POST_CODES = (
	('1', '1000'),
    ('2', '2000'),
    ('3', '3000'),
	('4', '4000'),
    ('5', '5000'),
    ('6', '6000'),
)
VRSTE_OBISKOV = (
	('1','Preventivni'),
	('2','Kurativni'),
)
VRSTE_OBISKOV_DETAIL = (
	('Obisk noseCnice', 'Obisk noseCnice'),
    ('Obisk otroCnice in novorojenCka', 'Obisk otroCnice in novorojenCka'),
    ('Preventivo starostnika', 'Preventivo starostnika'),
	('Odvzem krvi', 'Odvzem krvi'),
    ('Aplikacija injekcij', 'Aplikacija injekcij'),
    ('Kontrola zdravstvenega stanja', 'Kontrola zdravstvenega stanja'),
)
EPRUVETE_BARVA = (
	('Zelena', 'Zelena'),
    ('RDECA', 'RDECA'),
    ('MODRDA', 'MODRA'),
	('RUMENA', 'RUMENA'),
)
EPRUVETE_NUMBER = (
	('1', '1'),
    ('2', '2'),
    ('3', '3'),
	('4', '4'),
	('5', '5'),
)
class RegistrationFrom(forms.Form):
   cardNumber = forms.IntegerField(label='Stevilka kartice:', widget=forms.NumberInput(attrs={'id': 'cardNumber','placeholder':'04167496667'}))
   surname = forms.CharField(label='Priimek:', max_length=100, widget=forms.TextInput(attrs={'id': 'surname','placeholder': 'Novak'}))
   name = forms.CharField(label='Ime:', max_length=100, widget=forms.TextInput(attrs={'id': 'name','placeholder': 'Janez'}))
   address = forms.CharField(label='Naslov:', max_length=100, widget=forms.TextInput(attrs={'id': 'address','placeholder': 'Smartinska cesta 10'}))
   phone = forms.IntegerField(label='Telefon:', widget=forms.NumberInput(attrs={'id': 'phone','placeholder':'041674966'}))
   password = forms.CharField(label='Geslo',max_length=100, widget=forms.PasswordInput(attrs={'id': 'pass1'}))
   password2 = forms.CharField(label='Ponovi geslo',max_length=100, widget=forms.PasswordInput(attrs={'id': 'pass2'}))
   sex = forms.ChoiceField(choices=SEX_CHOICES)
   district = forms.ChoiceField(choices=DISTRICT_CHOICES)
   email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'uporabnik@gmail.com'}))
   birthDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker','id':'birthDate'}), input_formats=['%d-%m-%Y'])
   postCode =  forms.ChoiceField(label='PoSta',choices=POST_CODES)
   
   #kontaktna oseba
   contact_surname = forms.CharField(label='Priimek:',  required=False, max_length=100, widget=forms.TextInput(attrs={'id': 'contact_surname','placeholder': 'Novak'}))
   contact_name = forms.CharField(label='Ime:',  required=False, max_length=100, widget=forms.TextInput(attrs={'id': 'contact_name','placeholder': 'Janez'}))
   contact_address = forms.CharField(label='Naslov:', required=False,  max_length=100, widget=forms.TextInput(attrs={'id': 'contact_address'}))
   contact_phone_number = forms.IntegerField(label='Telefon',  required=False, widget=forms.NumberInput(attrs={'id': 'contact_phone_number','placeholder': '031890123'}))
   contact_sorodstvo = forms.CharField(label='relation:',  required=False, max_length=100, widget=forms.TextInput(attrs={'id': 'relation'}))
  

class AddNursingPatient(forms.Form):
	cardNumber = forms.IntegerField(label='Stevilka kartice:',widget=forms.NumberInput(attrs={'id': 'cardNumber'}))
	surname = forms.CharField(label='Priimek:', max_length=100, widget=forms.TextInput(attrs={'id': 'surname'}))
	name = forms.CharField(label='Ime:', max_length=100, widget=forms.TextInput(attrs={'id': 'name'}))
	address = forms.CharField(label='Naslov:', max_length=100, widget=forms.TextInput(attrs={'id': 'address'}))
	phone = forms.IntegerField(label='Telefon:', widget=forms.NumberInput(attrs={'id': 'phone'}))
	birthDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker','id':'birthDate'}), input_formats=['%d-%m-%Y'])
	postCode =  forms.ChoiceField(label='PoSta', choices=POST_CODES)
	sex = forms.ChoiceField(choices=SEX_CHOICES)
	district = forms.ChoiceField(choices=DISTRICT_CHOICES)
	relation = forms.ChoiceField(label='Sorodstvo:', choices = RELATIONS )
	
class WorkTaskForm(forms.Form):
	creatorId = forms.CharField(label='Stevilka zdravnika:', widget=forms.TextInput(attrs={'disabled': 'disabled'}))
	nurseId = forms.CharField(label='Stevilka izvajalca:', widget=forms.TextInput(attrs={'disabled': 'disabled'}))
	taskId = forms.CharField(label='Stevilka naloga:', widget=forms.TextInput(attrs={'disabled': 'disabled'}))
	visitType = forms.ChoiceField(choices=VRSTE_OBISKOV)
	visitTypeDetail = forms.ChoiceField(choices=VRSTE_OBISKOV_DETAIL,widget=forms.Select(attrs={'id':'visitType','onchange':'addPatientButton()'}))
	cardNumber = forms.CharField(label='Stevilka kartice:', max_length=100, widget=forms.NumberInput(attrs={'id': 'cardNumber'}))
	visitDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker','id':'visitDate','onchange':'firstVisitDate()'}), input_formats=['%d-%m-%Y'])
	visitCount = forms.CharField(label='Stevilo obiskov', max_length=100, widget=forms.NumberInput(attrs={'max': '10'}))
	timeInterval = forms.CharField(label='Casovni interval',widget=forms.TextInput(attrs={'id':'timeInterval'}))
	timePeriod = forms.CharField(label='Casovno obdobje',widget=forms.TextInput(attrs={'id':'timePeriod'}))
	
	#cureList = Zdravila.objects.all();
	
	cureId = forms.ChoiceField(choices=VRSTE_OBISKOV_DETAIL)
	materialColor = forms.ChoiceField(choices=EPRUVETE_BARVA)
	materialQuantity = forms.ChoiceField(choices=EPRUVETE_NUMBER,widget=forms.Select(attrs={'id':'stEpruvet'}))
	