import re

#   Izbrana vrednost za dolžino gesla
dolzina_gesla = 8


def dodaj_pacienta_skrbnik(geslo1, geslo2, ime, priimek, mail, st_kartice, naslov, st_okolisa, telefonska,
                           datum_rojstva, spol, kontakt_ime, kontakt_priimek, kontakt_naslov, kontakt_telefonska,
                           sorodstvo):

    if preveri_gesli(geslo1, geslo2):
        if preveri_email(mail):
            if preveri_kontakt(kontakt_ime, kontakt_priimek, kontakt_naslov, kontakt_telefonska, sorodstvo):
                if preveri_pacienta(ime, priimek, st_kartice, naslov, st_okolisa, telefonska):
                    #   DODAJ PACIENTA
                    
                    return 1
    return 0


def dodaj_pacienta_oskrbovanec():
    #   DODAJ PACIENTA
    #   DODAJ ODVISNOSTI
    return 0


#   Vrne 1, če vsebuje števko
def vsebuje_stevko(string):
    return any(char.isdigit() for char in string)


#   Preveri, ce je mail validen
def preveri_email(mail):
    if mail is not None:
        if re.match(r"[^@]+@[^@]+\.[^@]+", mail):
            return 1
    return 0


def preveri_pacienta(ime, priimek, st_kartice, naslov, st_okolisa, telefonska):
    if ime is not None\
            and priimek is not None\
            and naslov is not None\
            and st_kartice is not None\
            and st_okolisa is not None\
            and telefonska is not None:
        return 1
    return 0


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
                return 1
            return 0
    return 0


#   Preveri, če so vnešeni vsi podatki (in pravilno) oz če ni vnešeno nič (tudi validno)
def preveri_kontakt(ime, priimek, naslov, telefon, sorodstvo):
    if ime is None and priimek is None and naslov is None and telefon is None and sorodstvo is None:
        return 1
    elif ime is not None \
            and priimek is not None \
            and naslov is not None \
            and telefon is not None \
            and sorodstvo is not None:
        return 1
    return 0
