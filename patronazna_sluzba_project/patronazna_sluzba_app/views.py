#from django.contrib.auth import password_validation
import django.contrib.auth
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import validate_email
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse


from .forms import LoginForm, RegisterMedicalStaffForm
from .models import User,Vodja_PS,Zdravnik,Patronazna_sestra,Sodelavec_ZD,Pacient
import logging
from django.contrib.auth import password_validation
from .forms import LoginForm,RegistrationFrom,AddNursingPatient,ChangePasswordForm,WorkTaskForm
from .models import User,Vodja_PS,Zdravnik,Patronazna_sestra,Sodelavec_ZD,Pacient, Izvajalec_ZS,Zdravilo,Vrsta_obiska
from . import kreiranje_pacienta_zgodba2
from . import token
from ipware.ip import get_ip #pip install django-ipware
import os
import csv
from datetime import datetime
from django.contrib.auth import update_session_auth_hash

from dal import autocomplete
"""
class ZdraviloAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Zdravilo.objects.all()
        #if self.q:
        #    qs = qs.filter(name__istartswith=self.q)
        return qs
"""
def search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text =''

    medicine = Zdravilo.objects.filter(ime__contains=search_text)
    return render_to_response('ajax_search.html',{'medicine':medicine})

def search_patients(request):
    if request.method == 'POST':
        search_patient = request.POST['search_patient']
    else:
        search_patient =''

    patients = Pacient.objects.all()#filter(ime__contains=search_patient)
    return render_to_response('ajax_patient.html',{'patients':patients})

def choose_visit_type(request):
    if request.method == 'POST':
        choose_visit = request.POST['choose_visit']

    else:
        choose_visit = 'Preventivni obisk'

    visits = Vrsta_obiska.objects.filter(tip__contains=choose_visit)
    print('filter paremeter is: '+choose_visit)
    return render_to_response('ajax_visit.html',{'visits':visits})

#def index(request):
#
#   # if this is a POST request we need to process the form data
#    if request.method == 'POST':
#            #return HttpResponseRedirect('/thanks/')
#            return HttpResponse("Thanks, for trying.")
#    # if a GET (or any other method) we'll create a blank form
#    else:
#        form = LoginForm()
#
#    return render(request, 'index.html', {'login_form': form})
IP_FAILED_LOGIN=[]
BLACKLISTED_TIME_MIN=3
VAR = 0

context={}

# @login_required(login_url='/')
def workTaskForm(request):

    if request.method == 'POST':
        form = WorkTaskForm(request.POST)



        vrsta_obiska = request.POST['visitType']
        podvrsta_vrsta_obiska = request.POST['visitTypeDetail']


        prvi_obisk = request.POST['visitDate']

        try:
            if request.POST['mandatory']:
                obveznost = 'Obvezen'
        except:
            obveznost = 'Okviren'
        stevilo_obiskov = request.POST['visitCount']

        delovni_nalog = "Tip obiska: "+vrsta_obiska+"\nVrsta obiska details: "+podvrsta_vrsta_obiska+'\n'
        try:
            casovni_interval = request.POST['timeInterval']
        except:
            casovno_obdobje = request.POST['timePeriod']
        """
        if casovni_interval != '':
            print("casovni interval")
        else:
            casovno_obdobje = request.POST['timePeriod']
        """

        if podvrsta_vrsta_obiska == "Obisk otrocnice in novorojencka":
            print("obisk otrocnice")
            pacient_list = request.POST.getlist('addPatient')
            delovni_nalog+='Zavarovana oseba:\n'
            for i in pacient_list:
                print(i)
                delovni_nalog += '                '+i+'\n'

        else:
            pacient = request.POST['searchPatient']
            delovni_nalog += 'Zavarana oseba: '+ pacient+'\n'
            print('Pacient: '+pacient)
        if podvrsta_vrsta_obiska == 'Aplikacija injekcij':
            izbranaZdravila = request.POST.getlist('cureId')

            delovni_nalog += 'Izbrana zdravila:\n'
            for i in izbranaZdravila:
                print("Zdravilo " + i)
                delovni_nalog += '          '+i+'\n'
        elif podvrsta_vrsta_obiska == 'Odvzem krvi':
            print("odvzem krvi")

            delovni_nalog += 'Material:\n'
            izbran_material = request.POST.getlist('materialDN')
            for i in izbran_material:
                print('material: '+i)
                delovni_nalog += '          '+i+'\n'

        delovni_nalog += 'Datum prvega obiska: '+prvi_obisk+'\nObveznost obiska: '+obveznost+'\nStevilo obiskov: '+stevilo_obiskov+'\n'
        #zdravilo = request.POST['medicine']
        #autoData = request.POST['searchPatient']
        #pacient = autoData.split()
        return HttpResponse("Uspesno kreiranje delovnega naloga "+delovni_nalog);

    else:
        args = {}
        args.update(csrf(request))

        args['medicine'] = Zdravilo.objects.all()
        args['work_task_form'] = WorkTaskForm()
        #form = WorkTaskForm()

    return render(request, 'workTask.html', args)

def valid_login(ip):
    global IP_FAILED_LOGIN
    failed_ip_list = [x[0] for x in IP_FAILED_LOGIN]

    if len(IP_FAILED_LOGIN) > 0:
        if ip in failed_ip_list:
            print(ip)
            i = failed_ip_list.index(ip)
            del (IP_FAILED_LOGIN[i])
    else:
        return True


def invalid_login(ip):
    global IP_FAILED_LOGIN
    failed_ip_list = [x[0] for x in IP_FAILED_LOGIN]
    if ((len(IP_FAILED_LOGIN) > 0) and (ip in failed_ip_list)):
        i=failed_ip_list.index(ip)
        IP_FAILED_LOGIN[i][1]+=1
        if IP_FAILED_LOGIN[i][1]>=3:
            with open("IP_BLACKLIST.csv", "a+") as blacklist_file:
                blacklist_writer = csv.writer(blacklist_file,delimiter=';')
                blacklist_writer.writerow([ip,datetime.now()])
                blacklist_file.close()
    else:
        IP_FAILED_LOGIN.append([ip,1])



logger = logging.getLogger(__name__)

def ip_blacklisted(ip):
    global BLACKLISTED_TIME_MIN

    #DODAJ RAM CACHING, DA NE BO POTREBNO VEDNO BRATI CELOTNE DATOTEKE..
    if not os.path.isfile('IP_BLACKLIST.csv'):
        return False
    with open("IP_BLACKLIST.csv", "r") as blacklist_file:
        blacklist_reader = csv.reader(blacklist_file, delimiter=';')
        for line in blacklist_reader:
            if len(line) > 0:
                ip_naslov = line[0]  # 127.0.0.1;2017-04-13 20:34:17.582762
                cas_vnosa = datetime.strptime(line[1], "%Y-%m-%d %H:%M:%S.%f")
                pretekli_cas = (datetime.now() - cas_vnosa).total_seconds() / 60
                if pretekli_cas < BLACKLISTED_TIME_MIN:
                    if ip == ip_naslov:
                        return True
        return False

def isPatient(user):
    if Pacient.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def isNurse(user):
    if Patronazna_sestra.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def isDoctor(user):
    if Zdravnik.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def isLeaderPS(user):
    if Vodja_PS.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def isCoworker(user):
    if Sodelavec_ZD.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def isAdmin(user):
    return user.is_superuser

# Create your views here.
def index(request):
    global IP_FAILED_LOGIN

    ip_naslov=get_ip(request)
    if ip_blacklisted(ip_naslov):
        print("***IP naslov je bil zacasno blokiran, zaradi 3 neveljavnih poskusov prijave.")
        return HttpResponse("Vas IP naslov je blokiran, ponovno lahko poskusite cez 3 minute.")
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
                valid_login(ip_naslov)
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
                    return HttpResponseRedirect('base/controlPanel/')
            else:
                print("Unsuccessful user authentication.")
                print(IP_FAILED_LOGIN)
                invalid_login(ip_naslov)
                print(IP_FAILED_LOGIN)
                return HttpResponseRedirect('/')
        else:
            print("Invalid form!")
            return HttpResponseRedirect('/')
        return HttpResponse("Thanks for trying.")

@login_required(login_url='/')
def base(request):
    
    user=request.user
    if isAdmin(user):
        role="Admin"
    elif isCoworker(user):
        role="Sodelavec"
    elif isDoctor(user):
        role="Doktor"
    elif isLeaderPS(user):
        role="Vodja PS"
    elif isNurse(user):
        role="med.Sestra"
    else:
        role="pacient"

    if Pacient.objects.filter(uporabniski_profil=user).exists():
        pacient = Pacient.objects.get(uporabniski_profil=user)
        oskrbovanci = Pacient.objects.filter(skrbnistvo=pacient)


    print("base_function")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        #return HttpResponseRedirect('/thanks/')
        return HttpResponse("Thanks, for trying.")
        # if a GET (or any other method) we'll create a blank form
    else:
        global context
        context={'user_role': role, 'oskrbovanci_pacienta':oskrbovanci}
        # return render(request, 'medical_registration.html', context)
        #form = LoginForm()
        print("base_function")
        # return render(request, 'base.html')
        return render(request, 'base.html', context)
        # form = RegisterMedicalStaffForm()
        # return render(request, 'medical_registration.html', {'medical_reg_form': form})

# @user_passes_test(isAdmin,login_url='/')
def medicalStaffRegister(request):
    print("medical add")
    if request.method == 'GET':
        global context
        context={'medical_reg_form': RegisterMedicalStaffForm()}

        return render(request, 'medical_registration.html', context)
        # form = RegisterMedicalStaffForm()
        # return HttpResponse("THIS SHOULD BE IT.")
        # return render(request, 'medical_registration.html', {'medical_reg_form': form})
        # return render_to_response(request, 'medical_registration.html')
    else:
        #EXTRACT DATA FROM REQUEST
        #Extract standard user data from request

        form = RegisterMedicalStaffForm(request.POST)
        if form.is_valid():
            first_name =  form.cleaned_data['first_name']
            last_name =  form.cleaned_data['last_name']
            email =  form.cleaned_data['email']
            password1 = form.cleaned_data['password1']

            password2 =  form.cleaned_data['password2']
            # Extract additional staff specific data from request
            role =  form.cleaned_data['role']
            print("ROLE = ", role)
            code =  form.cleaned_data['medical_id']
            phone_number = form.cleaned_data['phone_number']
            institution =  form.cleaned_data["medical_area_id"]

            institution = Izvajalec_ZS.objects.filter(st_izvajalca=institution)
            # work_location_number=request.POST['work_location_number']
            if len(institution) == 0:
                institution = None
            else:
                institution = institution[0]

            # VALIDATE FIELD VALUES
            # Validate passwords
            # or not password_validation.validate_password(password1)
            if not password1 == password2 or not len(password1) > 7:
                print("Invalid password.")
            # Validate email
            if not kreiranje_pacienta_zgodba2.check_mail(email):
                print("Invalid email.")
            # Check if username(email) already exists
            if User.objects.filter(username=email).exists():
                print("Username is already taken.")
            # Check if nurse whith specified number already exists:
            if role == 'nurse' and Patronazna_sestra.objects.filter(sifra_patronazne_sestre=code).exists():
                print("Account with specified nurse number already exists.")
            elif role == 'doc' and Zdravnik.objects.filter(sifra_zdravnika=code):
                print("Account with specified doctor number already exists.")
            elif role == 'head_of_medical_service' and Vodja_PS.objects.filter(sifra_vodje_PS=code):
                print("Account with specified head of medical service number already exists.")
            elif role == 'employee' and Sodelavec_ZD.objects.filter(sifra_sodelavca=code):
                print("Account with specified employee number already exists.")
            # Validate phone number
            # Validate nurse number

            # CREATE AND SAVE NEW OBJECT TO DB
            # Create User object

            try:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password1,
                                                email=email,
                                                username=email)
                print("user object saved")
            except:
                print("Could not create User object using given data!")
                return HttpResponse("Userja ne gre registrirat.")
            # Finally create Nurse object

            if role == 'nurse':
                profile = Patronazna_sestra(uporabniski_profil=user, sifra_patronazne_sestre=code,
                                            telefonska_st=phone_number, sifra_izvajalca_ZS=institution)
                print("delam sestro")
            elif role == 'doc':
                profile = Zdravnik(uporabniski_profil=user, sifra_zdravnika=code, telefonska_st=phone_number,
                                   sifra_izvajalca_ZS=institution)
                print("delam zdravnika")
            elif role == 'head_of_medical_service':
                profile = Vodja_PS(uporabniski_profil=user, sifra_vodje_PS=code, telefonska_st=phone_number,
                                   sifra_izvajalca_ZS=institution)
                print("delam vodjo PS")
            elif role == 'employee':
                profile = Sodelavec_ZD(uporabniski_profil=user, ssifra_sodelavca=code, telefonska_st=phone_number,
                                       sifra_izvajalca_ZS=institution)
                print("delam sodelavec_ZD")

            print("profil:", profile.uporabniski_profil.username)
            profile.save()
            """
            try:
                profile.save()
            except:
                print("Could not create "+role+" profile using given data!")
            """

        return redirect('control_panel')

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
                user.is_active = 1
                pacient.save()
                print("Pacient je aktiviran")
                return HttpResponse("Aktivacija je uspesna. Prosimo, poizkusite se vpisati.")
            except:
                print("Ta mail ni v nasi bazi")

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

            uporabniki = User.objects.all()
            for i in uporabniki:
                if i.username == mail:
                    print("Ta mail je ze v bazi")
                    return HttpResponse("Ta mail je ze v bazi")

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
                return HttpResponse("Nekdo posile requeste napisane na roko... Ali pa ne dela vredu front end"
                                    " validacija... al pa mi funkcije ne palijo kot morjo :D")

            # poslji mail za aktivacijo
            act_key = token.generate_token(mail)

            kreiranje_pacienta_zgodba2.sendEmail(act_key.decode("utf-8"), mail)
            print("mail je poslan")

        else:
            print("Form not valid bro", form.errors)
            return HttpResponse("Form not valid")

        return redirect('home')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationFrom()

    return render(request, 'register.html', {'registration_form': form})

#@login_required(login_url='/')
def changePassword(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():

            currentUser = request.user
           # print("Uporabnik: ")
            oldpassword =  form.cleaned_data['oldpassword']
            #print(currentUser.check_password(oldpassword))
            if currentUser.check_password(oldpassword):
                password1 = form.cleaned_data['password1'];
                password2 = form.cleaned_data['password2'];
                if password1 == password2 and len(password1)>7:
                    request.user.set_password(password1)
                    update_session_auth_hash(request, request.user)
                    request.user.save()
                    return render(request, 'base.html', context)
                    #user = User.objects.get(username=currentUser)
                    #user.set_password(password1)
                    #user.save()
                else:
                    return HttpResponse("Napaka pri potrditvi novega gesla!")
            else:
                return HttpResponse("Napačen vnos trenutnega gesla!")

    else:
        form = ChangePasswordForm()
    return render(request, 'changePassword.html', {'change_password_form': form})



#@user_passes_test(isPatient,login_url='/')
def addNursingPatient(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = AddNursingPatient(request.POST)

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
            # return HttpResponse("Dodali ste oskrbovanca")
            return redirect('control_panel')
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


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

