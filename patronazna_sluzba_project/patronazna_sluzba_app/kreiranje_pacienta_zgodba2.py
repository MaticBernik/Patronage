import re
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
#   Izbrana vrednost za dolžino gesla
dolzina_gesla = 8
#   Dolzina stevilke kartice (11 glede na mojo kartico)
dolzina_card_number = 11
#   phone_number je lahko dolga max 15
dolzina_telefonske = 15


def add_patient_caretaker(password1, password2, name, surname, mail, card_number, address, phone_number,
                           birth_date, sex, contact_name, contact_surname, contact_address, contact_phone_number, sorodstveno_razmerje):

    if check_passwords(password1, password2):
        if check_mail_builtin(mail):
            if check_contact(contact_name, contact_surname, contact_address, contact_phone_number):
                if check_patient(name, surname, card_number, address, phone_number):
                    #   DODAJ PACIENTA
                    user = User.objects.create_user(username=mail,
                                                    password=password1)
                    print("user created")
                    if contact_name != "":
                        contact = Kontaktna_oseba(ime=contact_name, priimek=contact_surname,
                                                  naslov=contact_address, telefon=contact_phone_number)
                        contact.save()
                        print("contact saved")

                        patient = Pacient(uporabniski_profil=user, st_kartice=card_number, naslov=address,
                                          telefonska_st=phone_number,
                                          datum_rojstva=birth_date, spol=sex, kontakt=contact)
                        print("patient dodan")
                        patient.save()
                        print("patient saved")

                    else:
                        patient = Pacient(uporabniski_profil=user, st_kartice=card_number, naslov=address,
                                          telefonska_st=phone_number,
                                          datum_rojstva=birth_date, spol=sex)
                        print("patient dodan")
                        patient.save()

                        print("patient saved")

                    sorodstvo = Sorodstveno_razmerje(kontaktna_oseba=contact, pacient=patient, tip_razmerja=sorodstveno_razmerje)
                    sorodstvo.save()
                    print("sorodstvo saved")
                    return True
    return False


#   TUKAJ JE TREBA POSKRBET ŠE ZA SORODSTVA TER KO JE BAZA KONČANA PREVERIT ČE VSE DELA
def add_patient_taken_care_of(trenutni_uporabnik, name, surname, card_number, address,
                               birth_date, sex,
                               sorodstvo):

    if check_taken_care_of(name, surname, card_number, address):
        #   Tu dodam oskrbovanca
        patient = Pacient(uporabniski_profil=None, st_kartice=card_number, naslov=address,
                          telefonska_st="",
                          datum_rojstva=birth_date, spol=sex, kontakt=None, skrbnistvo=trenutni_uporabnik)
        patient.save()
        return True
    return False


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


def check_patient(name, surname, card_number, address, phone_number):
    if name is not None\
            and surname is not None\
            and address is not None\
            and card_number is not None\
            and phone_number is not None:
        if check_phone(phone_number) & check_card(card_number):
            return True

        return False
    print("Patient data should be... welll, filled out. (check_patient)")
    return False


def check_taken_care_of(name, surname, card_number, address, phone_number, sorodstvo):
    if name is not None\
            and surname is not None\
            and address is not None\
            and card_number is not None\
            and sorodstvo is not None\
            and phone_number is not None:
        if check_phone(phone_number) & check_card(card_number):
            return True
        return False
    return False


#   Prnamerja dve gesli, oba sta stringa. Funkcija vrne 1 če sta enaki in validni
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
    if isinstance(card_number, int):
        if len(str(card_number)) == dolzina_card_number:
            return True
        print("Card length not cool (check_card)")
        return False
    print("Card should be a number (check_card)")
    print(type(card_number))
    return False


def check_phone(phone_number):
    if isinstance(phone_number, int):
        if len(str(phone_number)) <= dolzina_telefonske:
            return True
        print("Phone length too... LONG (check_phone)")
        return False
    print("Phone number should be... you've guessed it... A FCKING NUMBER, BRO. (check_phone)")
    return False


#   Preveri, če so vnešeni vsi podatki (in pravilno) oz če ni vnešeno nič (tudi validno)
def check_contact(name, surname, address, telefon):
    if name == "" and surname == "" and address == "" and telefon is None:
        return 1
    elif name is not "" \
            and surname != "" \
            and address != "" \
            and telefon is not None:
        return True
    print("All or nothing. Contact, that is. (check_contact)")
    print(name)
    print(surname)
    print(address)
    print(telefon)
    return False


#   Vrne 1, če vsebuje števko
def contains_number(string):
    return any(char.isdigit() for char in string)
