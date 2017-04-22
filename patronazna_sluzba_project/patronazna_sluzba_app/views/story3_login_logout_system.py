#from django.contrib.auth import password_validation
from . import story2_create_patient
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, password_validation, update_session_auth_hash
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import validate_email
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.urls import reverse
from ipware.ip import get_ip #pip install django-ipware
from patronazna_sluzba_app import token
from patronazna_sluzba_app.forms import AddNursingPatientForm, ChangePasswordForm, LoginForm, PatientRegistrationFrom, RegisterMedicalStaffForm, WorkTaskForm
from patronazna_sluzba_app.models import Izvajalec_ZS, Pacient, Patronazna_sestra, Sodelavec_ZD, User, Vodja_PS, Zdravnik
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
import csv
import django.contrib.auth
import logging
import os
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

def is_patient(user):
    if Pacient.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def is_nurse(user):
    if Patronazna_sestra.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def is_doctor(user):
    if Zdravnik.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def is_leader_ps(user):
    if Vodja_PS.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def is_coworker(user):
    if Sodelavec_ZD.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def is_admin(user):
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

def base(request):
    
    user=request.user
    if is_admin(user):
        role="Admin"
    elif is_coworker(user):
        role="Sodelavec"
    elif is_doctor(user):
        role="Doktor"
    elif is_leader_ps(user):
        role="Vodja PS"
    elif is_nurse(user):
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

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
