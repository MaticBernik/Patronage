# -*- coding: utf-8 -*-
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from patronazna_sluzba_app import token
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from patronazna_sluzba_app.forms import *
from django.template import Context, loader, RequestContext

import hashlib
import random
import re
#   Izbrana vrednost za dolzino gesla
dolzina_gesla = 8
#   Dolzina stevilke kartice (9+3=12 glede na mojo kartico)
dolzina_card_number = 12
#   phone_number je lahko dolga max 15
dolzina_telefonske = 15


def search_post_code(request):
    if request.method == 'POST':
        search_post = request.POST['search_post']
    else:
        search_post =''

    #post = Posta.objects.all()
    post = Posta.objects.filter(naziv_poste__icontains=search_post)[:20]
    return render_to_response('ajax_post.html',{'post':post})

def search_district_name(request):

    post_code = "1000"
    if request.method == 'POST':
        # preberi posto, ki je izbrana
        #print("POST FROM DISTRICT")
        chosen_post = request.POST['search_post']
        post_code = chosen_post.split()
        post_code = post_code[0]
        #print("POST Code is: "+post_code)
        search_district = request.POST['search_district']
    else:
        search_district =''
        #print("District GET: ")
    #print('Posta ajax '+post_code)
    district = Okolis.objects.filter(posta_id=post_code).filter(ime__icontains=search_district)
    return render_to_response('ajax_district.html',{'district':district})

def add_patient_caretaker(password1, password2, first_name, last_name, mail, card_number, address, phone_number,
                           birth_date, sex, contact_first_name, contact_last_name, contact_address, contact_phone_number, sorodstveno_razmerje, posta, district):

    if check_passwords(password1, password2):
        if check_mail_builtin(mail):
            if check_contact(contact_first_name, contact_last_name, contact_address, contact_phone_number):
                if check_patient(first_name, last_name, card_number, address, phone_number):
                    #   DODAJ PACIENTA

                    if contact_first_name != "":

                        patient = Pacient(ime=first_name, priimek=last_name, st_kartice=card_number, naslov=address,
                                          telefonska_st=phone_number,
                                          datum_rojstva=birth_date, spol=sex, email=mail, posta=posta, okolis=district)
                        print("patient objekt ustvarjen")


                        print("sorodstvo saved")

                        user = User.objects.create_user(username=mail,
                                                        password=password1,
                                                        email=mail, is_active=0)

                        patient.uporabniski_profil = user


                        patient.save()

                        contact = Kontaktna_oseba(ime=contact_first_name, priimek=contact_last_name,
                                                  naslov=contact_address, telefon=contact_phone_number)
                        contact.save()

                        sorodstvo = Sorodstveno_razmerje(kontakt=contact, pacient_id=patient, tip_razmerja=sorodstveno_razmerje)
                        sorodstvo.save()

                        contact.sorodstvo = sorodstvo
                        contact.save()

                        patient.sorodstvo = sorodstvo
                        patient.save()

                        patient.kontakt = contact
                        patient.save()
                        print("user created")
                        print("patient saved")
                    else:
                        patient = Pacient(ime=first_name, priimek=last_name, st_kartice=card_number, naslov=address,
                                          telefonska_st=phone_number,
                                          datum_rojstva=birth_date, spol=sex, email=mail, posta=posta, okolis=district)
                        print("patient dodan")
                        #patient.save()

                        user = User.objects.create_user(username=mail,
                                                        password=password1,
                                                        email=mail, is_active=0)

                        patient.uporabniski_profil = user
                        patient.save()
                        print("user created")

                        print("patient saved")


                        # mail verifikacija

                    return True
    return False


def add_patient_taken_care_of(trenutni_uporabnik, first_name, last_name, card_number, address,
                               birth_date, sex,
                               sorodstvo, phone_number):

    if check_taken_care_of(first_name, last_name, card_number, address, phone_number, sorodstvo):
        #   Tu dodam oskrbovanca
        patient = Pacient(uporabniski_profil=None, st_kartice=card_number, naslov=address, ime=first_name, priimek=last_name,
                          telefonska_st=phone_number,
                          datum_rojstva=birth_date, spol=sex, kontakt=None, skrbnistvo=trenutni_uporabnik)
        patient.save()
        print("Dodan oskrbovanec za: ", trenutni_uporabnik.uporabniski_profil.username)

        oskrbovanci = Pacient.objects.filter(skrbnistvo=trenutni_uporabnik)
        for i in oskrbovanci:
            print("Oskrbovanceva kartica je: ", i.st_kartice)
        return True
    return False


def sendEmail(activation_key, customer_mail):

    link="http://127.0.0.1:8000/activate?token="+activation_key
    sporocilo = "Greetings. Thank you for working with PARSEK. We would like to ask you to click the link below for email verification.  "+link+" Have a nice day. Parsek team."
    msg = """\
    <html>
      <head></head>
      <body>
        <p>Lep pozdrav!<br>
           Hvala za sodelovanje.<br>
           Sledite tej <a href=""" + link + """">povezavi</a> za aktivacijo vašega računa .
        </p>        
        <hr>
           Lep pozdrav, Parsek.<br>
        </p>
      </body>
    </html>
    """
    send_mail(
        'Parsek RULES. You will want to activate',
        msg,
        'activation@parsekrules.si',
        [customer_mail],
        fail_silently=False,
        html_message=msg
    )
    print("mail poslan")




#   Preveri, ce je mail validen
def check_mail(mail):
    if mail is not None:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
            return True
    return False


#   Uporabi to funkcijo povsod ter jo pretestiraj
def check_mail_builtin(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        print("Email is wrong. WOOONG. (check_mail_builtin)")
        return False


def check_patient(first_name, last_name, card_number, address, phone_number):
    if first_name is not None\
            and last_name is not None\
            and address is not None\
            and card_number is not None\
            and phone_number is not None:
        if check_phone_number(phone_number) & check_card(card_number):
            return True
        print("returnam false")
        return False
    print("Patient data should be... welll, filled out. (check_patient)")
    return False


def check_taken_care_of(first_name, last_name, card_number, address, phone_number, sorodstvo):
    if first_name is not None\
            and last_name is not None\
            and address is not None\
            and card_number is not None\
            and sorodstvo is not None\
            and phone_number is not None:
        if check_phone_number(phone_number) & check_card(card_number):
            return True
        return False
    print("Taken care of dude data not cool.")
    return False


#   Primerja dve gesli, oba sta stringa. Funkcija vrne 1 ce sta enaki in validni
def check_passwords(password1, password2):
    if password1 == password2:
        stevilo_crk1 = 0
        stevilo_crk2 = 0

        for crka in password1:
            stevilo_crk1 += 1
        for crka in password2:
            stevilo_crk2 += 1

        if stevilo_crk1 >= dolzina_gesla and stevilo_crk2 >= dolzina_gesla:
            if contains_number(password1):
                if password_validation.validate_password(password1) is None:
                    return True
                else:
                    print(ValidationError.args)
                    print("Built in password validation error (check_passwords)")
                return False
            print("Password should have numbers (check_passwords)")
            return False
    print("Password just doesn't work (check_passwords)")
    print("Password 1:", password1)
    print("Password 2:", password2)
    return False


def check_card(card_number):
    #if isinstance(card_number, int):
        if len(str(card_number)) == dolzina_card_number:
            try:
                st_kartice = Pacient.objects.get(card_number=card_number)
                print("This card number is already in the database.")
                return False
            except:
                return True
        print("Card length not cool (check_card)")
        return False
    #print("Card should be a number (check_card)")
        print(type(card_number))
        return False


def check_phone_number(phone_number):
    if isinstance(phone_number, int):
        if len(str(phone_number)) <= dolzina_telefonske:
            return True
        print("phone_number length too... LONG (check_phone_number)")
        return False
    print("phone_number number should be... you've guessed it... A FCKING NUMBER, BRO. (check_phone_number)")
    return False


#   Preveri, ce so vneseni vsi podatki (in pravilno) oz ce ni vneseno nic (tudi validno)
def check_contact(first_name, last_name, address, telefon):
    if first_name == "" and last_name == "" and address == "" and telefon is None:
        return 1
    elif first_name is not "" \
            and last_name != "" \
            and address != "" \
            and telefon is not None:
        return True
    print("All or nothing. Contact, that is. (check_contact)")
    print(first_name)
    print(last_name)
    print(address)
    print(telefon)
    return False


#   Vrne 1, ce vsebuje stevko
def contains_number(string):
    return any(char.isdigit() for char in string)
    
    
def register_patient(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        form = PatientRegistrationFrom(request.POST)

        if form.is_valid():
            #   Preveri, da kartice slucajno ze ne obstaja.
            card_number = form.cleaned_data['card_number']
            try:
                st_kartice = Pacient.objects.get(card_number=card_number)
                print("This card number is already in the database.")
                return HttpResponse("This card number is already in our database. You may have gotten it wrong?")
            except:
                print("Card number is not in our DB yet, all good.")

            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mail = form.cleaned_data['email']

            uporabniki = User.objects.all()
            for i in uporabniki:
                if i.username == mail:
                    print("Ta mail je ze v bazi")
                    return HttpResponse("Ta mail je ze v bazi")

            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            birth_date = form.cleaned_data['birth_date']
            sex = form.cleaned_data['sex']
            contact_first_name = form.cleaned_data['contact_first_name']
            contact_last_name = form.cleaned_data['contact_last_name']
            contact_address = form.cleaned_data['contact_address']
            contact_phone_number = form.cleaned_data['contact_phone_number']
            sorodstveno_razmerje = form.cleaned_data['contact_sorodstvo']

            #uspesno izbrana posta
            postal_num = request.POST['search_post']
            print('izbrana posta '+postal_num)
            # uspesno izbran okolis
            district = request.POST['search_district']
            okolis = Okolis.objects.get(ime=district)

            posta = Posta.objects.get(postna_st=int(postal_num[:4]))

            print('izbrana posta ' + district)

            if not (add_patient_caretaker(password1, password2, first_name, last_name, mail,

                                                                    card_number, address, phone_number,
                                                                    birth_date, sex, contact_first_name,
                                                                    contact_last_name, contact_address,
                                                                    contact_phone_number, sorodstveno_razmerje, posta, okolis)):
                return HttpResponse("Nekdo posile requeste napisane na roko... Ali pa ne dela vredu front end"
                                    " validacija... al pa mi funkcije ne palijo kot morjo :D")

            # poslji mail za aktivacijo
            act_key = token.generate_token(mail)

            sendEmail(act_key.decode("utf-8"), mail)
            print("mail je poslan")

        else:
            print("Form not valid bro", form.errors)
            return HttpResponse("Form not valid")

        return redirect('/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = PatientRegistrationFrom()

    return render(request, 'patient_registration.html', {'registration_form': form})


#@user_passes_test(isPatient,login_url='/')
def add_nursing_patient(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = AddNursingPatientForm(request.POST)

        """
        pacienti = Pacient.objects.all()
        for i in pacienti:
            print(i.st_kartice)
"""
        # za testiranje
        # current_user = User.objects.get(username="stoklas.nac@gmail.com")
        current_user = request.user
        current_pacient = Pacient.objects.get(uporabniski_profil=current_user)
        print("TUKAAAAJ", current_user.username)

        #current_pacient = Pacient.objects.get(uporabniski_profil=request.user)

        if form.is_valid():
            #   Preveri, da kartice slucajno ze ne obstaja.
            card_number = form.cleaned_data['card_number']
            try:
                st_kartice = Pacient.objects.get(st_kartice=card_number)
                print("This card number is already in the database. Number:", st_kartice)
                return HttpResponse("This card number is already in our database. You may have gotten it wrong?")
            except:
                print("Card number is not in our DB yet, all good.")

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            #postCode = form.cleaned_data['post_code']
            #posta oskrbovanca
            post_code = request.POST['search_post']
            district_name = request.POST['search_district']
            print('posta oskrbovanca '+post_code +' okolis '+district_name)
            #district = form.cleaned_data['district']
            birth_date = form.cleaned_data['birth_date']
            sex = form.cleaned_data['sex']
            relation = form.cleaned_data['relation']

            if not (
                    add_patient_taken_care_of(current_pacient, first_name, last_name, card_number,
                                                                         address,
                                                                          birth_date, sex, relation, phone_number)):
                return HttpResponse("Napaka pri dodajanju oskrbovanca");
            # return HttpResponse("Dodali ste oskrbovanca")
            return redirect('link_control_panel')
        """ DEJANSKA KODA ko bo se front end naret
        if form.is_valid():
            if request.user.is_authenticated():
                currentUser = request.user.username
                card_number = form.cleaned_data['card_number']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                address = form.cleaned_data['address']
                postCode = form.cleaned_data['postCode']
                district = form.cleaned_data['district']
                birth_date = form.cleaned_data['birth_date']
                sex = form.cleaned_data['sex']
                relation = form.cleaned_data['relation']

                if not (
                kreiranje_pacienta_zgodba2.add_patient_taken_care_of(currentUser, first_name, last_name, card_number, address,
                                                                     district, birth_date, sex, relation)):
                    return HttpResponse("Napaka pri dodajanju oskrbovanca");
        return HttpResponse("Dodali ste oskrbovanca")
        """
    else:
        nursing_patient_form = AddNursingPatientForm()
        return render(request, 'add_nursing_patient.html', {'add_nursing_patient_form': nursing_patient_form, 'nbar': 'add_nursing'})

    
