import re
from .models import *
#   Izbrana vrednost za dolžino gesla
dolzina_gesla = 8
#   Dolzina stevilke kartice (11 glede na mojo kartico)
dolzina_st_kartice = 11
#   Telefonska je lahko dolga max 15
dolzina_telefonske = 15


def dodaj_pacienta_skrbnik(geslo1, geslo2, ime, priimek, mail, st_kartice, naslov, st_okolisa, telefonska,
                           datum_rojstva, spol, kontakt_ime, kontakt_priimek, kontakt_naslov, kontakt_telefonska):

    if preveri_gesli(geslo1, geslo2):
        if preveri_email(mail):
            if preveri_kontakt(kontakt_ime, kontakt_priimek, kontakt_naslov, kontakt_telefonska):
                if preveri_pacienta(ime, priimek, st_kartice, naslov, st_okolisa, telefonska):
                    #   DODAJ PACIENTA
                    user = User.objects.create_user(username=mail,
                                                    password=geslo1,
                                                    email=mail)

                    kontakt = Kontaktna_oseba(ime=kontakt_ime, priimek=kontakt_priimek,
                                              naslov=kontakt_naslov, telefon=kontakt_telefonska)
                    kontakt.save()

                    pacient = Pacient(uporabniski_profil=user, st_kartice=st_kartice, naslov=naslov,
                                      st_okolisa=st_okolisa, telefonska_st=telefonska,
                                      datum_rojstva=datum_rojstva, spol=spol, kontakt=kontakt)
                    pacient.save()
                    return True
    return False


#   TUKAJ JE TREBA POSKRBET ŠE ZA SORODSTVA TER KO JE BAZA KONČANA PREVERIT ČE VSE DELA
def dodaj_pacienta_oskrbovanec(trenutni_uporabnik, ime, priimek, st_kartice, naslov, st_okolisa,
                               datum_rojstva, spol,
                               sorodstvo):

    if preveri_oskrbovanca(ime, priimek, st_kartice, naslov, st_okolisa):
        #   Tu dodam oskrbovanca
        pacient = Pacient(uporabniski_profil=None, st_kartice=st_kartice, naslov=naslov,
                          st_okolisa=st_okolisa, telefonska_st="",
                          datum_rojstva=datum_rojstva, spol=spol, kontakt=None, skrbnistvo=trenutni_uporabnik)
        pacient.save()
        return True
    return False


#   Preveri, ce je mail validen
def preveri_email(mail):
    if mail is not None:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
            return True
    return False


def preveri_pacienta(ime, priimek, st_kartice, naslov, st_okolisa, telefonska):
    if ime is not None\
            and priimek is not None\
            and naslov is not None\
            and st_kartice is not None\
            and st_okolisa is not None\
            and telefonska is not None:
        if preveri_telefonsko(telefonska) & preveri_kartico(st_kartice):
            return True
        return False
    return False


def preveri_oskrbovanca(ime, priimek, st_kartice, naslov, st_okolisa, telefonska, sorodstvo):
    if ime is not None\
            and priimek is not None\
            and naslov is not None\
            and st_kartice is not None\
            and st_okolisa is not None\
            and sorodstvo is not None\
            and telefonska is not None:
        if preveri_telefonsko(telefonska) & preveri_kartico(st_kartice):
            return True
        return False
    return False


#   Primerja dve gesli, oba sta stringa. Funkcija vrne 1 če sta enaki in validni
def preveri_gesli(geslo1, geslo2):
    if geslo1 == geslo2:
        stevilo_crk1 = 0
        stevilo_crk2 = 0

        for crka in geslo1:
            stevilo_crk1 += 1
        for crka in geslo2:
            stevilo_crk2 += 1

        if stevilo_crk1 >= dolzina_gesla and stevilo_crk2 >= dolzina_gesla:
            if vsebuje_stevko(geslo1):
                return True
            return False
    return False


def preveri_kartico(st_kartice):
    if isinstance(st_kartice, int):
        if len(str(st_kartice)) == dolzina_st_kartice:
            return True
        return False
    return False


def preveri_telefonsko(telefonska):
    if isinstance(telefonska, int):
        if len(str(telefonska)) <= dolzina_telefonske:
            return True
        return False
    return False


#   Preveri, če so vnešeni vsi podatki (in pravilno) oz če ni vnešeno nič (tudi validno)
def preveri_kontakt(ime, priimek, naslov, telefon):
    if ime is None and priimek is None and naslov is None and telefon is None:
        return 1
    elif ime is not None \
            and priimek is not None \
            and naslov is not None \
            and telefon is not None:
        return True
    return False


#   Vrne 1, če vsebuje števko
def vsebuje_stevko(string):
    return any(char.isdigit() for char in string)
