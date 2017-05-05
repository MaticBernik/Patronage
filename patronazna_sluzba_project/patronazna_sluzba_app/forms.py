# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

from .models import *
from django.core.validators import MaxValueValidator
from django.db.models import When, F, Q, Case
from django.forms import  ModelForm

USER_TYPES = (
    ('doc', 'Zdravnik'),
    ('nurse', 'Medicinska sestra / brat'),
    ('head_of_medical_service', 'Vodja patronažne službe'),
    ('employee', 'Uslužbenec zdravstvene ustanove'),
)

SEX_CHOICES = (
    ('1', 'Moški'),
    ('2', 'Zenški'),
)

DISTRICT_CHOICES = (
    ('1', '05600 - VIČ-RUDNIK'),
    ('2', '05470 - ŠIŠKA'),
    ('3', '05030 - BEŽIGRAD'),
    ('4', '05300 - MOSTE-POLJE'),
)

RELATIONS = (
    ('1', 'Oče / mama'),
    ('2', 'Otrok'),
    ('3', 'Vnuk'),
    ('4', 'Dedek / babica'),
    ('5', 'Brat / sestra'),
)

POST_CODES = (
    ('1', '1000'),
    ('2', '2000'),
    ('3', '3000'),
    ('4', '4000'),
    ('5', '5000'),
    ('6', '6000'),
)
VRSTE_OBISKOV =[
    ('#',''),
    ('Preventivni obisk','Preventivni obisk'),
    ('Kurativni obisk','Kurativni obisk'),
]
VRSTE_OBISKOV_DETAIL = (
    ('Obisk nosecnice', 'Obisk nosecnice'),
    ('Obisk otrocnice in novorojenCka', 'Obisk otrocnice in novorojencka'),
    ('Preventivo starostnika', 'Preventivo starostnika'),
    ('Odvzem krvi', 'Odvzem krvi'),
    ('Aplikacija injekcij', 'Aplikacija injekcij'),
    ('Kontrola zdravstvenega stanja', 'Kontrola zdravstvenega stanja'),
)

EPRUVETE_BARVA = (
    ('Zelena', 'Zelena'),
    ('Rdeca', 'Rdeca'),
    ('Modra', 'Modra'),
    ('Rumena', 'Rumena'),
)

EPRUVETE_NUMBER = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

# SOME VALIDATORS
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
numberic_only = RegexValidator(r'^[0-9]*$', 'Dovoljena zgolj stevilska vrednost.')
min_len_12 = MinLengthValidator(12, "Stevilka kartica je dolzine 12 znakov.")
max_len_12 = MaxLengthValidator(12, "Stevilka kartica je dolzine 12 znakov.")

#so far the conditionst are very basic, to be strickend
class LoginForm(forms.Form):
    username = forms.CharField(label='Uporabniško ime:', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Geslo:', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterMedicalStaffForm(forms.Form):
    # check medical_id length, same for medical_area_id and phone_number_id
    medical_id = forms.IntegerField(label='Šifra zdravstvenega osebja: ', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Ime: ', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Priimek: ', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    medical_area_id = forms.IntegerField(label='Šifra zdravstvenega okoliša: ', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-poštni naslov: ', max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(label='Telefonska številka: ', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Geslo: ', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Ponovite geslo: ', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    medic_role = forms.ChoiceField(label='Tip zdravstvenega uslužbenca: ', choices=USER_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))


class PatientRegistrationFrom(forms.Form):
    # card_number = forms.IntegerField(label='Številka zdravstvene kartice: ', widget=forms.NumberInput(attrs={'id': 'card_number','placeholder':'Sifra zdrav. kartice (12 mest)', 'class': 'form-control'}))
    card_number = forms.CharField(label='Številka zdravstvene kartice: ', validators=[numberic_only, min_len_12, max_len_12], widget=forms.NumberInput(attrs={'id': 'card_number','placeholder':'Sifra zdrav. kartice (12 mest)', 'class': 'form-control'}))
    last_name = forms.CharField(label='Priimek: ', max_length=100, widget=forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control'}))
    first_name = forms.CharField(label='Ime: ', max_length=100, widget=forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control'}))
    address = forms.CharField(label='Naslov: ', max_length=100, widget=forms.TextInput(attrs={'id': 'address', 'class': 'form-control'}))
    phone_number = forms.IntegerField(label='Telefonska številka: ', widget=forms.NumberInput(attrs={'id': 'phone','placeholder':'xxxxxxxxx', 'class': 'form-control'}))
    password = forms.CharField(label='Geslo: ',max_length=100, widget=forms.PasswordInput(attrs={'id': 'pass1', 'class': 'form-control'}))
    password2 = forms.CharField(label='Ponovite geslo: ',max_length=100, widget=forms.PasswordInput(attrs={'id': 'pass2', 'class': 'form-control'}))
    sex = forms.ChoiceField(label='Spol: ', choices=SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    #district = forms.ChoiceField(label='Okrožje: ', choices=DISTRICT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-poštni naslov: ', widget=forms.EmailInput(attrs={'placeholder':'uporabnik@gmail.com', 'class': 'form-control'}))
    birth_date = forms.DateField(label='Rojstni datum: ', widget=forms.TextInput(attrs={'class':'datepicker form-control','id':'birth_date'}), input_formats=['%d.%m.%Y'])
    # UPDATE REQUIRED -> POSTAL CODE AND CITY -> TWO AUTOCOMPLETE FIELDS
    #post_code =  forms.ChoiceField(label='Pošta: ',choices=POST_CODES, widget=forms.Select(attrs={'class': 'form-control'}))

    #kontaktna oseba
    contact_last_name = forms.CharField(label='Priimek: ',  required=False, max_length=100, widget=forms.TextInput(attrs={'id': 'contact_last_name', 'class': 'form-control'}))
    contact_first_name = forms.CharField(label='Ime: ',  required=False, max_length=100, widget=forms.TextInput(attrs={'id': 'contact_first_name', 'class': 'form-control'}))
    contact_address = forms.CharField(label='Naslov: ', required=False,  max_length=100, widget=forms.TextInput(attrs={'id': 'contact_address', 'class': 'form-control'}))
    contact_phone_number = forms.IntegerField(label='Telefonska številka: ',  required=False, widget=forms.NumberInput(attrs={'id': 'contact_phone_number','placeholder': 'xxxxxxxxx', 'class': 'form-control'}))
    contact_sorodstvo = forms.ChoiceField(label='Sorodstveno razmerje: ',  required=False, choices = RELATIONS, widget=forms.Select(attrs={'id': 'relation', 'class': 'form-control'} ))

class AddNursingPatientForm(forms.Form):
    card_number = forms.IntegerField(label='Številka kartice osebe: ',widget=forms.NumberInput(attrs={'id': 'card_number', 'class': 'form-control'}))
    last_name = forms.CharField(label='Priimek: ', max_length=100, widget=forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control'}))
    first_name = forms.CharField(label='Ime: ', max_length=100, widget=forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control'}))
    address = forms.CharField(label='Naslov: ', max_length=100, widget=forms.TextInput(attrs={'id': 'address', 'class': 'form-control'}))
    phone_number = forms.IntegerField(label='Telefon: ', widget=forms.NumberInput(attrs={'id': 'phone', 'class': 'form-control'}))
    birth_date = forms.DateField(label='Datum rojstva: ', widget=forms.TextInput(attrs={'class':'datepicker form-control','id':'birth_date'}), input_formats=['%d.%m.%Y'])
    #post_code =  forms.ChoiceField(label='Pošta: ', choices=POST_CODES, widget=forms.Select(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='Spol: ', choices=SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    #district = forms.ChoiceField(label='Okrožje', choices=DISTRICT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    relation = forms.ChoiceField(label='Sorodstveno razmerje: ', choices = RELATIONS, widget=forms.Select(attrs={'class': 'form-control'} ))

class WorkTaskForm(forms.Form):

    creator_id = forms.CharField(label='Številka zdravnika: ', widget=forms.TextInput(attrs={'disabled': 'disabled', 'class': 'form-control'}))
    nurse_id = forms.ChoiceField(choices=[],label='Številka izvajalca: ')
    task_id = forms.CharField(label='Številka naloga: ', widget=forms.TextInput(attrs={'disabled': 'disabled', 'class': 'form-control'}))
    #visit_type = forms.ChoiceField(label='Vrsta obiska: ', choices=VRSTE_OBISKOV, widget=forms.Select(attrs={'class': 'form-control','id':'choose-visit'}))
    #visit_type_detail = forms.ChoiceField(label='Vrsta storitve: ', choices=VRSTE_OBISKOV_DETAIL,widget=forms.Select(attrs={'id':'visit_type','onchange':'addPatientButton()', 'class': 'form-control'}))
    visitType = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'id': 'choose-visit'}))
    visitTypeDetail = forms.ChoiceField(choices=[], widget=forms.Select(
        attrs={'id': 'visitType', 'onchange': 'addPatientButton()'}))
    #card_number = forms.CharField(label='Številka kartice: ', max_length=100, widget=forms.NumberInput(attrs={'id': 'card_number', 'class': 'form-control'}))
    #visit_date = forms.DateField(label='Datum obiska', widget=forms.TextInput(attrs={'class':'datepicker form-control','id':'visit_date','onchange':'firstVisitDate()'}), input_formats=['%d.%m.%Y'])
    #visit_count = forms.CharField(label='Število obiskov: ', max_length=100, widget=forms.NumberInput(attrs={'max': '10', 'class': 'form-control'}))
    #time_interval = forms.CharField(label='Časovni interval: ', widget=forms.TextInput(attrs={'id':'time_interval', 'class': 'form-control'}))
   # time_period = forms.CharField(label='Časovno obdobje: ', widget=forms.TextInput(attrs={'id':'time_period', 'class': 'form-control'}))

    addPatient = forms.MultipleChoiceField(choices=[], required=False)

    visitDate = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker', 'id': 'visitDate'}),
        input_formats=['%d.%m.%Y'])
    mandatory = forms.BooleanField(required=False)
    visitCount = forms.CharField(label='Stevilo obiskov', max_length=100, widget=forms.NumberInput(attrs={'max': '10'}))

    timeInterval = forms.CharField(label='Casovni interval', widget=forms.NumberInput(attrs={'id': 'timeInterval'}))
    timePeriod = forms.CharField(label='Casovno obdobje', widget=forms.NumberInput(attrs={'id': 'timePeriod'}))

    # cureList = Zdravila.objects.all();

    cureId = forms.MultipleChoiceField(choices=[], required=False)

    # izbira materilov
    materialColor = forms.ChoiceField(label='Barva epruvete: ',choices=EPRUVETE_BARVA)
    materialQuantity = forms.ChoiceField(label='Število epruvet: ',choices=EPRUVETE_NUMBER, widget=forms.Select(attrs={'id': 'stEpruvet'}))

    materialDN = forms.MultipleChoiceField(label='Izbran material ',choices=[], required=False)


    #cureList = Zdravila.objects.all();
   # cure_id = forms.ChoiceField(label='Vrsta storitve: ', choices=VRSTE_OBISKOV_DETAIL, widget=forms.Select(attrs={'class': 'form-control'}))
    #test_tube_color = forms.ChoiceField(label='Barva epruvete: ', choices=EPRUVETE_BARVA, widget=forms.Select(attrs={'class': 'form-control'}))
    #test_tube_quantity = forms.ChoiceField(label='Število epruvet: ', choices=EPRUVETE_NUMBER,widget=forms.Select(attrs={'id':'st_epruvet', 'class': 'form-control'}))

    #lets try ajax master/detail
#visitType = forms.ChoiceField(choices=VRSTE_OBISKOV,widget=forms.Select(attrs={'id':'choose-visit'}))

#visitTypeDetail = forms.ChoiceField(choices=[],widget=forms.Select(attrs={'id':'visitType','onchange':'addPatientButton()'}))
#spremenjeno, zdaj se isce po imenu s ajax
#cardNumber = forms.CharField(label='Stevilka kartice:', max_length=100, widget=forms.NumberInput(attrs={'id': 'cardNumber'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Trenutno geslo: ', max_length=100, widget=forms.PasswordInput(attrs={'id': 'old_pass', 'class': 'form-control'}))
    new_password1 = forms.CharField(label='Novo geslo: ', max_length=100, widget=forms.PasswordInput(attrs={'id': 'new_pass', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Ponovite geslo: ', max_length=100, widget=forms.PasswordInput(attrs={'id': 'new_pass2', 'class': 'form-control'}))

class plan_visit_form(forms.Form):
    visit_list = forms.MultipleChoiceField(required=False, label='Neopravljeni obiski',choices=[],widget=forms.SelectMultiple(attrs={'class': 'form-control','id':'visit_list'}))
    plan_list = forms.MultipleChoiceField(required=False, label='Izbrani obiski',choices=[],widget=forms.SelectMultiple(attrs={'class': 'form-control'}))