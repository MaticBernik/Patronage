# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

from .models import *
from django.core.validators import MaxValueValidator
from django.db.models import When, F, Q, Case
from django.forms import  ModelForm
from django.contrib.auth.models import User

USER_TYPES = (
    ('doc', 'Zdravnik'),
    ('nurse', 'Medicinska sestra / brat'),
    ('head_of_medical_service', 'Vodja patronažne službe'),
    ('employee', 'Uslužbenec zdravstvene ustanove'),
)

SEX_CHOICES = (
    ('Moški', 'Moški'),
    ('Zenški', 'Zenški'),
)

DISTRICT_CHOICES = (
    ('1', '05600 - VIČ-RUDNIK'),
    ('2', '05470 - ŠIŠKA'),
    ('3', '05030 - BEŽIGRAD'),
    ('4', '05300 - MOSTE-POLJE'),
)

RELATIONS = (
    ('Oce / mama', 'Oce / mama'),
    ('Otrok', 'Otrok'),
    ('Vnuk', 'Vnuk'),
    ('Dedek / babica', 'Dedek / babica'),
    ('Brat / sestra', 'Brat / sestra'),
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

OPRAVLJENOST_OBISKA = (
    (-1,'---------'),
    (1, 'Opravljen'),
    (0, 'Neopravljen'),
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
    date_picker = forms.DateField(required=False,label='Izberi datum',widget=forms.TextInput(attrs={'class': 'datepicker form-control', 'id': 'date_picker'}),input_formats=['%d.%m.%Y'])

class FilterWorkTasksForm(forms.Form):
    '''staff_members=[x.id for x in User.objects.filter(is_staff=1)]
    filter_creator_id = forms.ModelChoiceField(label='Šifra izdajatelja naloga: ', required = False, queryset=User.objects.filter(profil_id__in=staff_members), widget=forms.Select(attrs={'disabled': 'disabled', 'class': 'input-sm form-control'}))
    '''

    # filter_creator_id = forms.CharField(label='Šifra izdajatelja naloga: ', required = False, widget=forms.TextInput(attrs={'disabled': 'disabled', 'class': 'input-sm form-control'}))
    # filter_creator_id = forms.ModelChoiceField(label='Šifra izdajatelja naloga: ', required = False, queryset=User.objects.filter(is_staff=1), widget=forms.Select(attrs={'disabled': 'disabled', 'class': 'input-sm form-control'}))
    filter_creator_id = forms.ModelChoiceField(label='Šifra izdajatelja DN: ', required = False, queryset=Uporabnik.objects.all(), widget=forms.Select(attrs={'class': 'input-sm form-control'}))
    # filter_nurse_id = forms.CharField(label='Šifra med. sestre: ', required = False, widget=forms.TextInput(attrs={'disabled': 'disabled', 'class': 'input-sm form-control'}))
    # filter_nurse_id = forms.ModelChoiceField(label='Šifra med. sestre: ', required = False, queryset=Patronazna_sestra.objects.all(), widget=forms.Select(attrs={'disabled': 'disabled', 'class': 'input-sm form-control'}))
    filter_nurse_id = forms.ModelChoiceField(label='Šifra med. sestre: ', required = False, queryset=Patronazna_sestra.objects.all(), widget=forms.Select(attrs={'class': 'input-sm form-control'}))
    # filter_patient_id = forms.CharField(label='Šifra zdravnika: ', widget=forms.TextInput(attrs={'disabled': 'disabled', 'class': 'form-control'}))
    filter_patient_id = forms.ModelChoiceField(label='Pacient', required = False, queryset=Pacient.objects.all(), widget=forms.Select(attrs={'class': 'input-sm form-control', 'id': 'select_patient_filter'}))
    # filter_visit_type = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'id': 'task_visit_type'}))
    filter_visit_type = forms.ModelChoiceField(label='Vrsta obiska', required = False, queryset=Vrsta_obiska.objects.all(), widget=forms.Select(attrs={'class': 'input-sm form-control', 'id': 'task_visit_type_filter'}))

    filter_date_from = forms.DateField(label='Datum od:', required = False,
        widget=forms.TextInput( attrs={'class': 'datepicker input-group date input-sm form-control', 'id': 'task_date_from'}),
        input_formats=['%d.%m.%Y'])
    filter_date_to = forms.DateField(label='Datum do:', required = False,
        widget=forms.TextInput( attrs={'class': 'datepicker input-group date input-sm  form-control', 'id': 'task_date_to'}),
        input_formats=['%d.%m.%Y'])


class FilterVisitationsForm(forms.Form):

    filter_creator_id = forms.ModelChoiceField(label='Šifra izdajatelja DN: ', required = False, queryset=Uporabnik.objects.all(), widget=forms.Select(attrs={'class': 'input-sm form-control'}))
    
    filter_nurse_id = forms.ModelChoiceField(label='Šifra med. sestre: ', required = False, queryset=Patronazna_sestra.objects.all(), widget=forms.Select(attrs={'class': 'input-sm form-control'}))

    filter_substitute_nurse_id = forms.ModelChoiceField(label='Šifra nad. med. sestre: ', required = False, queryset=Patronazna_sestra.objects.none(), widget=forms.Select(attrs={'class': 'input-sm form-control'}))
    
    filter_patient_id = forms.ModelChoiceField(label='Pacient', required = False, queryset=Pacient.objects.all(), widget=forms.Select(attrs={'class': 'input-sm form-control', 'id': 'select_patient_filter'}))
    
    filter_visit_type = forms.ModelChoiceField(label='Vrsta obiska', required = False, queryset=Vrsta_obiska.objects.all(), widget=forms.Select(attrs={'class': 'input-sm form-control', 'id': 'task_visit_type_filter'}))
   
    # filter_visit_complete = forms.ModelChoiceField(label='Opravljenost obiska', required = False, queryset=["Opravljen","Ni opravljen"], widget=forms.Select(attrs={'class': 'input-sm form-control', 'id': 'visitation_mandatory_filter'}))
    filter_visit_complete = forms.ChoiceField(label='Opravljenost obiska', required = False, choices=OPRAVLJENOST_OBISKA, widget=forms.Select(attrs={'class': 'input-sm form-control', 'id': 'visitation_mandatory_filter'}))
    
    filter_date_from = forms.DateField(label='Datum od:', required = False,
        widget=forms.TextInput( attrs={'class': 'datepicker input-group date input-sm form-control', 'id': 'task_date_from'}),
        input_formats=['%d.%m.%Y'])
    filter_date_to = forms.DateField(label='Datum do:', required = False,
        widget=forms.TextInput( attrs={'class': 'datepicker input-group date input-sm  form-control', 'id': 'task_date_to'}),
        input_formats=['%d.%m.%Y'])

class SubstituteSisterForm(forms.Form):
    start_date = forms.DateField(label='Začetek', widget=forms.TextInput(
        attrs={'class': 'datepicker form-control', 'id': 'start_date'}), input_formats=['%d.%m.%Y'])

    end_date = forms.DateField(label='Konec', widget=forms.TextInput(
        attrs={'class': 'datepicker form-control', 'id': 'end_date'}), input_formats=['%d.%m.%Y'])
#queryset = Pacient.objects.get(posta_id=1000)
class EditProfileForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditProfileForm, self).__init__(*args, **kwargs)
        queryset = Pacient.objects.select_related().get(uporabniski_profil=self.user)

        self.fields['card_number'] = forms.CharField(disabled=True,label='Številka zdravstvene kartice: ',
                                  validators=[numberic_only, min_len_12, max_len_12], widget=forms.NumberInput(
            attrs={'id': 'card_number', 'placeholder': 'Sifra zdrav. kartice (12 mest)', 'class': 'form-control','value':queryset.st_kartice}))
        self.fields['last_name'] = forms.CharField(label='Priimek: ', max_length=100,
                                    widget=forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control','value':queryset.priimek}))
        self.fields['first_name'] = forms.CharField(label='Ime: ', max_length=100,
                                     widget=forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control','value':queryset.ime}))
        self.fields['address'] = forms.CharField(label='Naslov: ', max_length=100,
                                  widget=forms.TextInput(attrs={'id': 'address', 'class': 'form-control','value':queryset.naslov}))
        self.fields['phone_number'] = forms.IntegerField(label='Telefonska številka: ', widget=forms.NumberInput(
            attrs={'id': 'phone', 'placeholder': 'xxxxxxxxx', 'class': 'form-control','value':queryset.telefonska_st}))
        """
        password = forms.CharField(label='Geslo: ', max_length=100,
                                   widget=forms.PasswordInput(attrs={'id': 'pass1', 'class': 'form-control'}))
        password2 = forms.CharField(label='Ponovite geslo: ', max_length=100,
                                    widget=forms.PasswordInput(attrs={'id': 'pass2', 'class': 'form-control'}))
        """
        self.fields['sex'] = forms.CharField(disabled=True,label='Spol: ',widget=forms.TextInput(attrs={'class': 'form-control','value':queryset.spol}))
        # district = forms.ChoiceField(label='Okrožje: ', choices=DISTRICT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['email'] = forms.EmailField(disabled=True,label='E-poštni naslov: ', widget=forms.EmailInput(
            attrs={'placeholder': 'uporabnik@gmail.com', 'class': 'form-control','value':queryset.email}))
        self.fields['birth_date']  = forms.DateField(disabled=True,label='Rojstni datum: ', widget=forms.TextInput(
            attrs={'class': 'datepicker form-control', 'id': 'birth_date','value':formatDate(queryset.datum_rojstva)}), input_formats=['%d.%m.%Y'])


        if queryset.kontakt != None:
            self.fields['contact_last_name'] = forms.CharField(label='Priimek: ',  required=False, max_length=100, widget=forms.TextInput(attrs={'id': 'contact_last_name', 'class': 'form-control','value':queryset.kontakt.priimek}))
            self.fields['contact_first_name'] = forms.CharField(label='Ime: ',  required=False, max_length=100, widget=forms.TextInput(attrs={'id': 'contact_first_name', 'class': 'form-control','value':queryset.kontakt.ime}))
            self.fields['contact_address'] = forms.CharField(label='Naslov: ', required=False,  max_length=100, widget=forms.TextInput(attrs={'id': 'contact_address', 'class': 'form-control','value':queryset.kontakt.naslov}))
            self.fields['contact_phone_number'] = forms.IntegerField(label='Telefonska številka: ',  required=False, widget=forms.NumberInput(attrs={'id': 'contact_phone_number','placeholder': 'xxxxxxxxx', 'class': 'form-control','value':queryset.kontakt.telefon}))
            self.fields['contact_sorodstvo'] = forms.ChoiceField(label='Sorodstveno razmerje: ', required=False,
                                                                 choices=RELATIONS,
                                                                 initial=queryset.kontakt.sorodstvo.tip_razmerja,
                                                                 widget=forms.Select(
                                                                     attrs={'id': 'relation', 'class': 'form-control'}))
        else:
            self.fields['contact_last_name'] = forms.CharField(label='Priimek: ', required=False, max_length=100,
                                                               widget=forms.TextInput(attrs={'id': 'contact_last_name',
                                                                                             'class': 'form-control',
                                                                                             }))
            self.fields['contact_first_name'] = forms.CharField(label='Ime: ', required=False, max_length=100,
                                                                widget=forms.TextInput(
                                                                    attrs={'id': 'contact_first_name',
                                                                           'class': 'form-control'}))
            self.fields['contact_address'] = forms.CharField(label='Naslov: ', required=False, max_length=100,
                                                             widget=forms.TextInput(attrs={'id': 'contact_address',
                                                                                           'class': 'form-control'}))
            self.fields['contact_phone_number'] = forms.IntegerField(label='Telefonska številka: ', required=False,
                                                                     widget=forms.NumberInput(
                                                                         attrs={'id': 'contact_phone_number',
                                                                                'placeholder': 'xxxxxxxxx',
                                                                                'class': 'form-control'}))
            self.fields['contact_sorodstvo'] = forms.ChoiceField(label='Sorodstveno razmerje: ', required=False,
                                                                 choices=RELATIONS, widget=forms.Select(
                    attrs={'id': 'relation', 'class': 'form-control'}))

class EditNursingProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditNursingProfileForm, self).__init__(*args, **kwargs)
        queryset = Pacient.objects.select_related().get(st_kartice=self.user)

        self.fields['card_number'] = forms.IntegerField(disabled=True,label='Številka kartice osebe: ',
                                         widget=forms.NumberInput(attrs={'id': 'card_number', 'class': 'form-control','value':queryset.st_kartice}))
        self.fields['last_name'] = forms.CharField(label='Priimek: ', max_length=100,
                                    widget=forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control','value':queryset.priimek}))
        self.fields['first_name'] = forms.CharField(label='Ime: ', max_length=100,
                                     widget=forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control','value':queryset.ime}))
        self.fields['address'] = forms.CharField(label='Naslov: ', max_length=100,
                                  widget=forms.TextInput(attrs={'id': 'address', 'class': 'form-control','value':queryset.naslov}))
        self.fields['phone_number'] = forms.IntegerField(label='Telefon: ',
                                          widget=forms.NumberInput(attrs={'id': 'phone', 'class': 'form-control','value':queryset.telefonska_st}))
        self.fields['birth_date'] = forms.DateField(disabled=True,label='Datum rojstva: ',
                                     widget=forms.TextInput(attrs={'class': 'datepicker form-control', 'id': 'birth_date','value':formatDate(queryset.datum_rojstva)}),
                                     input_formats=['%d.%m.%Y'])
        self.fields['sex'] = forms.CharField(disabled=True,label='Spol: ', widget=forms.TextInput(attrs={'class': 'form-control','value':queryset.spol}))


def formatDate(datum):
    myDate = str(datum).split(" ",1)
    temp = myDate[0].split('-')
    newDate = temp[2]+'.'+temp[1]+'.'+temp[0]
    return newDate

class ForgottenPasswordForm(forms.Form):
    email = forms.EmailField(label='E-poštni naslov: ', max_length=50,widget=forms.EmailInput(attrs={'class': 'form-control','id':'reset_mail'}))
    new_password1 = forms.CharField(label='Novo geslo: ', max_length=100, widget=forms.PasswordInput(attrs={'id': 'reset_password1', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Ponovite geslo: ', max_length=100, widget=forms.PasswordInput(attrs={'id': 'reset_password2', 'class': 'form-control'}))

class SubstitutionFinishedForm(forms.Form):
    absent = Nadomescanje.objects.filter(nadomestna_sestra_id=6).filter(veljavno=True).values_list('sestra_id',flat=True)
    # preveri ali sestra, ki jo nadomecam že nadomešča drugo sestro
    print("================FORMS.PY===============")
    print(absent)
    print("=======================================")
    for x in absent:
        absent |= Nadomescanje.objects.filter(nadomestna_sestra_id=x).filter(veljavno=True).values_list('sestra_id',flat=True)

    print("================FORMS.PY===============")
    print(absent)
    print("=======================================")
    query = Nadomescanje.objects.filter(veljavno =True).values_list("sestra_id",flat=True)
    query_nurses = Patronazna_sestra.objects.filter(id__in=query)
    nurses = forms.ModelChoiceField(label='Odsotne sestre: ', queryset=query_nurses,widget=forms.Select(attrs={'class': 'form-control'}))
