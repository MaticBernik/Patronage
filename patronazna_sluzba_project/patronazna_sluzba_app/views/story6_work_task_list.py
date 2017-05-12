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
from patronazna_sluzba_app.models import Izvajalec_ZS, Pacient, Patronazna_sestra, Sodelavec_ZD, User, Vodja_PS, Zdravnik, Obisk, Delovni_nalog, Pacient_DN, Material_DN, Zdravilo_DN
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
    filter_form = FilterWorkTasksForm()
    uporabnik = request.user
    vklopi_filtre=True
    if is_doctor(uporabnik):
        izdajatelj=Zdravnik.objects.get(uporabniski_profil=uporabnik)
        delovni_nalogi = Delovni_nalog.objects.filter(zdravnik=izdajatelj.sifra_zdravnika)
        filter_form.fields['filter_creator_id'].initial = izdajatelj
    elif is_leader_ps(uporabnik):
        izdajatelj=Vodja_PS.objects.get(uporabniski_profil=uporabnik)
        vklopi_filtre=False
        delovni_nalogi = Delovni_nalog.objects.filter(vodja_PS=izdajatelj.sifra_vodje_PS)
        filter_form.fields['filter_creator_id'].initial = izdajatelj
    elif is_nurse(uporabnik):
        nurse=Patronazna_sestra.objects.get(uporabniski_profil=uporabnik)
        pacienti = Pacient.objects.filter(okolis_id=nurse.okolis_id)
        nalogi_vezani_na_pacienta=Pacient_DN.objects.filter(pacient_id__in=pacienti)
        delovni_nalogi = Delovni_nalog.objects.filter(id__in=[x.delovni_nalog_id for x in nalogi_vezani_na_pacienta])
        #filter_form.fields['filter_nurse_id']=nurse
        filter_form.fields['filter_nurse_id'].initial=str(nurse.sifra_patronazne_sestre)+" "+nurse.uporabniski_profil.first_name+" "+nurse.uporabniski_profil.last_name

        #DODAJ FILTER
    else:
        print("ERROR!!")
        return

    form=FilterWorkTasksForm(request.POST)
    if not form.is_valid():
        print("ERROR: FORM NOT VALID")

    if request.POST:
        if request.POST.get('filter_date_from',0):
            datum = datetime.strptime(request.POST['filter_date_from'], "%d.%m.%Y")
            delovni_nalogi = delovni_nalogi.filter(datum_prvega_obiska__gte=datum) #datetime.max
            #filter_form.fields['filter_date_from'] = request.POST['filter_date_from']
            filter_form.fields['filter_date_from'].initial = request.POST['filter_date_from']
        if request.POST.get('filter_date_to',0):
            datum = datetime.strptime(request.POST['filter_date_to'], "%d.%m.%Y")
            delovni_nalogi = delovni_nalogi.filter(datum_prvega_obiska__lte=datum) #datetime.min
            #filter_form.fields['filter_date_to'] = request.POST['filter_date_to']
            filter_form.fields['filter_date_to'].initial = request.POST['filter_date_to']
        if request.POST.get('filter_visit_type',0):
            delovni_nalogi = delovni_nalogi.filter(vrsta_obiska_id=request.POST['filter_visit_type'])
            #filter_form.fields['filter_visit_type'] = request.POST['filter_visit_type']
            filter_form.fields['filter_visit_type'].initial=request.POST['filter_visit_type']
        if request.POST.get('filter_patient_id',0):
            print(type(request.POST['filter_patient_id']))
            pacientDN=Pacient_DN.objects.filter(pacient_id=request.POST['filter_patient_id'])
            nalogi_vezani_na_pacienta=[x.delovni_nalog_id for x in pacientDN]
            delovni_nalogi = delovni_nalogi.filter(id__in=nalogi_vezani_na_pacienta)
            #filter_form.fields['filter_patient_id'] = request.POST['filter_patient_id']
            filter_form.fields['filter_patient_id'].initial=request.POST['filter_patient_id']
        if request.POST.get('filter_nurse_id',0):
            nurse = Patronazna_sestra.objects.get(uporabniski_profil=uporabnik)
            pacienti = Pacient.objects.filter(okolis_id=nurse.okolis_id)
            nalogi_vezani_na_pacienta = Pacient_DN.objects.filter(pacient_id__in=pacienti)
            delovni_nalogi = Delovni_nalog.objects.filter(id__in=[x.delovni_nalog_id for x in nalogi_vezani_na_pacienta])
            filter_form.fields['filter_nurse_id'].initial = str(nurse.sifra_patronazne_sestre) + " " + nurse.uporabniski_profil.first_name + " " + nurse.uporabniski_profil.last_name

    if not vklopi_filtre:
        delovni_nalogi=Delovni_nalog.objects.all();
    visitations = Obisk.objects.all()
    #  FORM QUERY SET
    # form.fields['adminuser'].queryset = User.objects.filter(account=accountid)
    #filter_creator_id
    #filter_nurse_id
    #filter_patient_id
    #filter_visit_type
    material = Material_DN.objects.all()
    #zdravila = Zdravilo_DN.objects.all()
    pacienti = Pacient_DN.objects.all()
    
    
    context = {'work_task_list':delovni_nalogi, 'visits_list':visitations, 'nbar': 'v_wrk_tsk', 'filter_form': filter_form, 'material': material, 'pacient': pacienti  }
    return render(request, 'work_task_list.html', context)

