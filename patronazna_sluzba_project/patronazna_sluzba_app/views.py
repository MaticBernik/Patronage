from django.shortcuts import render

# Create your views here.


#   Izbrana vrednost za dolžino gesla
dolzina_gesla = 8


#   Vrne 1, če vsebuje števko
def vsebuje_stevko(string):
    return any(char.isdigit() for char in string)


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
