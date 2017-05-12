# -*- coding: utf-8 -*-
# @login_required(login_url='/')
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
from patronazna_sluzba_app.forms import AddNursingPatientForm, ChangePasswordForm, LoginForm, PatientRegistrationFrom, RegisterMedicalStaffForm, WorkTaskForm, FilterWorkTasksForm
from patronazna_sluzba_app.models import Izvajalec_ZS, Pacient, Patronazna_sestra, Sodelavec_ZD, User, Vodja_PS, Zdravnik, Obisk, Delovni_nalog, Pacient_DN
import csv
import django.contrib.auth
import logging
import os

def is_doctor(user):
    if Zdravnik.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def is_leader_ps(user):
    if Vodja_PS.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def is_nurse(user):
    if Patronazna_sestra.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def list_work_task(request):
    uporabnik = request.user
    obiski = Obisk.objects
    
    """if is_doctor(uporabnik):
        izdajatelj=Zdravnik.objects.get(uporabniski_profil=uporabnik)
        delovni_nalogi = Delovni_nalog.objects.filter(zdravnik=izdajatelj)
    elif is_leader_ps(uporabnik):
        izdajatelj=Vodja_PS.objects.filter(uporabniski_profil=uporabnik)
        delovni_nalogi = Delovni_nalog.objects.filter(vodja_PS=izdajatelj)
    elif is_nurse(uporabnik):
        nurse=Patronazna_sestra.objects.get(uporabniski_profil=uporabnik)
        #DODAJ FILTER
    else:
        print("ERROR!!")
        return

    if request.filter_datum_zacetni:
        delovni_nalogi = delovni_nalogi.filter(datum_prvega_obiska__range=(request.filter_datum_zacetni, request.filter_datum_koncni))
    if request.filter_datum_koncni:
        delovni_nalogi = delovni_nalogi.filter(datum_prvega_obiska__range=(request.filter_datum_zacetni, request.filter_datum_koncni))
    if request.filter_vrsta_obiska:
        delovni_nalogi = delovni_nalogi.filter(vrsta_obiska_id=request.filter_vrsta_obiska)
    if request.filter_pacient:
        pacientDN=Pacient_DN.objects.filter(pacient_id=request.filter_pacient)
        nalogi_vezani_na_pacienta=[x.delovni_nalog_id for x in pacientDN]
        delovni_nalogi = delovni_nalogi.filter(id__in=nalogi_vezani_na_pacienta)
    #if request.filter_patronazna_sestra
    """
    if(request.POST.get("value") == "expand"):
        print("expand please")
    print('name' in request.POST)


    filter_form = FilterWorkTasksForm()
    obiski = Obisk.objects.all()
    delovni_nalogi = Delovni_nalog.objects.all()
    #  FORM QUERY SET
    # form.fields['adminuser'].queryset = User.objects.filter(account=accountid)

    context = {'work_task_list':delovni_nalogi, 'visits_list':obiski, 'nbar': 'v_wrk_tsk', 'filter_form': filter_form }
    return render(request, 'work_task_list.html', context)

