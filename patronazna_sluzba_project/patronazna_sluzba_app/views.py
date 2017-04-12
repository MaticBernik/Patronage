#from django.contrib.auth import password_validation
import django.contrib.auth
from django.core.validators import validate_email
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
#from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import *
from .models import User,Vodja_PS,Zdravnik,Patronazna_sestra,Sodelavec_ZD,Pacient
from . import kreiranje_pacienta_zgodba2
from . import token

#def index(request):
#
#	# if this is a POST request we need to process the form data
#    if request.method == 'POST':
#            #return HttpResponseRedirect('/thanks/')
#            return HttpResponse("Thanks, for trying.")
#    # if a GET (or any other method) we'll create a blank form
#    else:
#        form = LoginForm()
#
#    return render(request, 'index.html', {'login_form': form})



# Create your views here.
def index(request):
    if request.method=='GET':
        form = LoginForm()

        return render(request, 'index.html', {'login_form': form})
    elif request.method=='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            print('Login: ',username)
            if user is not None:

                u = User.objects.get(username=username)
                if Pacient.objects.filter(uporabniski_profil=u).exists():
                    pacient = Pacient.objects.get(uporabniski_profil=u)
                    if pacient.aktiviran == 0:
                        return HttpResponse("Potrebna je aktivacija uporabniskega racuna pacienta.")


                login(request, user)
                if Patronazna_sestra.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_nurse/')
                elif Vodja_PS.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_ps_leader/')
                elif Zdravnik.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_doctor/')
                elif Sodelavec_ZD.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_employee/')
                elif Pacient.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_patient/')
            else:
                print("Unsuccessful user authentication.")
                return HttpResponseRedirect('/')
        else:
            print("Invalid form!")
            return HttpResponseRedirect('/')
        return HttpResponse("Thanks for trying.")


def activate(request):
    if request.method == 'GET':
        act_key = request.GET.get('token', '')
        if act_key != '':

            print("Token value is: ")
            value = token.is_valid_token(act_key)
            print(value)

            try:
                user = User.objects.get(username=value)
                pacient = Pacient.objects.get(uporabniski_profil=user)
                pacient.aktiviran = 1
                pacient.save()
                print("Pacient je aktiviran")
                return HttpResponse("Aktivacija je uspesna. Prosimo, poizkusite se vpisati.")
            except:
                print("Ta mail ni v naši bazi")

    return HttpResponse("Aktivacija ni uspela.")


def register(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        form = RegistrationFrom(request.POST)

        if form.is_valid():
            #   Preveri, da kartice slucajno ze ne obstaja.
            card_number = form.cleaned_data['cardNumber']
            try:
                st_kartice = Pacient.objects.get(card_number=card_number)
                print("This card number is already in the database.")
                return HttpResponse("This card number is already in our database. You may have gotten it wrong?")
            except:
                print("Card number is not in our DB yet, all good.")



            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            mail = form.cleaned_data['email']

            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone']
            birth_date = form.cleaned_data['birthDate']
            sex = form.cleaned_data['sex']
            contact_name = form.cleaned_data['contact_name']
            contact_surname = form.cleaned_data['contact_surname']
            contact_address = form.cleaned_data['contact_address']
            contact_phone_number = form.cleaned_data['contact_phone_number']
            sorodstveno_razmerje = form.cleaned_data['contact_sorodstvo']

            if not (kreiranje_pacienta_zgodba2.add_patient_caretaker(password1, password2, name, surname, mail,
                                                                    card_number, address, phone_number,
                                                                    birth_date, sex, contact_name,
                                                                    contact_surname, contact_address,
                                                                    contact_phone_number, sorodstveno_razmerje)):
                return HttpResponse("Nekdo posile requeste napisane na roko... al pa mi se funkcije ne delajo")

            # poslji mail za aktivacijo
            act_key = token.generate_token(mail)

            kreiranje_pacienta_zgodba2.sendEmail(act_key.decode("utf-8"), mail)

        else:
            print("form not valid bro", form.errors)
            return HttpResponse("Form not valid")

        return HttpResponse("Registracija uspela")


    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationFrom()

    return render(request, 'register.html', {'registration_form': form})


def changePassword(request):

    return render(request, 'changePassword.html')


def addNursingPatient(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = AddNursingPatient(request.POST)

        pacienti = Pacient.objects.all()
        for i in pacienti:
            print(i.st_kartice)

        # za testiranje
        current_user = User.objects.get(username="test@gmail.com")
        current_pacient = Pacient.objects.get(uporabniski_profil=current_user)
        print(current_user.username)

        if form.is_valid():
            #   Preveri, da kartice slucajno ze ne obstaja.
            cardNumber = form.cleaned_data['cardNumber']
            try:
                st_kartice = Pacient.objects.get(st_kartice=cardNumber)
                print("This card number is already in the database. Number:", st_kartice)
                return HttpResponse("This card number is already in our database. You may have gotten it wrong?")
            except:
                print("Card number is not in our DB yet, all good.")

            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            postCode = form.cleaned_data['postCode']
            district = form.cleaned_data['district']
            birthDate = form.cleaned_data['birthDate']
            sex = form.cleaned_data['sex']
            relation = form.cleaned_data['relation']

            if not (
                    kreiranje_pacienta_zgodba2.add_patient_taken_care_of(current_pacient, name, surname, cardNumber,
                                                                         address,
                                                                          birthDate, sex, relation, phone)):
                return HttpResponse("Napaka pri dodajanju oskrbovanca");
            return HttpResponse("Dodali ste oskrbovanca")
        """ DEJANSKA KODA ko bo se front end naret
        if form.is_valid():
            if request.user.is_authenticated():
                currentUser = request.user.username
                cardNumber = form.cleaned_data['cardNumber']
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                postCode = form.cleaned_data['postCode']
                district = form.cleaned_data['district']
                birthDate = form.cleaned_data['birthDate']
                sex = form.cleaned_data['sex']
                relation = form.cleaned_data['relation']

                if not (
                kreiranje_pacienta_zgodba2.add_patient_taken_care_of(currentUser, name, surname, cardNumber, address,
                                                                     district, birthDate, sex, relation)):
                    return HttpResponse("Napaka pri dodajanju oskrbovanca");
        return HttpResponse("Dodali ste oskrbovanca")
        """
    else:
        form = AddNursingPatient()
        return render(request, 'addNursingPatient.html', {'add_nursing_patient': form})