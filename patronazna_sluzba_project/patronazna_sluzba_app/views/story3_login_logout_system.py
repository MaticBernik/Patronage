# -*- coding: utf-8 -*-
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
import csv
import django.contrib.auth
import logging
import os

IP_FAILED_LOGIN=[]
BLACKLISTED_TIME_MIN=3
BLACKLIST_ATTEMPTS_BEFORE_LOCK=5
VAR = 0

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
        if IP_FAILED_LOGIN[i][1]>=BLACKLIST_ATTEMPTS_BEFORE_LOCK:
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

def get_patient_role_string():

    if is_patient(user):
        return "patient"
    elif is_nurse(user):
        return "nurse"
    elif is_doctor(user):
        return "doctor"
    elif is_leader_ps(user):
        return "nursing_officer"
    elif is_coworker(user):
        return "coworker"
    elif is_admin(user):
        return "admin"
    else:
        return "unknown_user_type"

# Create your views here.
def index(request):
    global IP_FAILED_LOGIN

    ip_naslov=get_ip(request)
    if ip_blacklisted(ip_naslov):
        print("***IP naslov je bil zacasno blokiran, zaradi 3 neveljavnih poskusov prijave.")
        form = LoginForm(request.POST)
        #return HttpResponse("Vas IP naslov je blokiran, ponovno lahko poskusite cez 3 minute.")
        return render(request, 'index.html', {'login_form': form, 'blocked': True})
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
                    if u.is_active == 0:
                        #return HttpResponse("Potrebna je aktivacija uporabniskega racuna pacienta.")
                        return render(request, 'index.html', {'login_form': form, 'not_verified': True})

                login(request, user)
                return HttpResponseRedirect(reverse('link_control_panel'))
            else:
                print("Unsuccessful user authentication.")
                print(IP_FAILED_LOGIN)
                invalid_login(ip_naslov)
                print(IP_FAILED_LOGIN)
                #return HttpResponseRedirect('/')
                return render(request, 'index.html', {'login_form': form, 'wrong_data': True})
        else:
            print("Invalid form!")
            #return HttpResponseRedirect('/')
            return render(request, 'index.html', {'login_form': form, 'invalid': True})
        return HttpResponse("Thanks for trying.")

def base(request):
    
    print("base_function")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        #return HttpResponseRedirect('/thanks/')
        return HttpResponse("Thanks, for trying.")
        # if a GET (or any other method) we'll create a blank form
    else:
        context={'nbar': 'ctrl_panel'}
        # return render(request, 'medical_registration.html', context)
        # Assign role-based navbar
        #form = LoginForm()
        print("base_function")
        # return render(request, 'base.html')
        # return render(request, 'base.html', context)
        return render(request, 'base_panel.html', context)
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
                user.is_active = 1
                user.save()
                print("Pacient je aktiviran")
                form = LoginForm()
                #return HttpResponse("Aktivacija je uspesna. Prosimo, poizkusite se vpisati.")
                return render(request, 'index.html', {'login_form': form, 'registered_success': True})
            except:
                print("Ta mail ni v nasi bazi")

    return HttpResponse("Aktivacija ni uspela.")
    #return render(request, 'index.html', {'login_form': form, 'not_verified': True})
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def empty(request):
    return render(request, 'empty.html')