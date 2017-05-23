# -*- coding: utf-8 -*-
# @login_required(login_url='/')
from datetime import datetime,timedelta
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
from patronazna_sluzba_app.forms import AddNursingPatientForm, ChangePasswordForm, LoginForm, PatientRegistrationFrom, RegisterMedicalStaffForm, WorkTaskForm, FilterVisitationsForm
from patronazna_sluzba_app.models import Izvajalec_ZS, Pacient, Patronazna_sestra, Sodelavec_ZD, User, Vodja_PS, Zdravnik, Obisk, Delovni_nalog, Pacient_DN, Material_DN, Zdravilo_DN, Uporabnik
import csv
import django.contrib.auth
import logging
import os

def is_doctor(user):
    if Zdravnik.objects.filter(uporabniski_profil_id=user).exists():
        return True
    return False

def is_leader_ps(user):
    if Vodja_PS.objects.filter(uporabniski_profil_id=user).exists():
        return True
    return False

def is_nurse(user):
    if Patronazna_sestra.objects.filter(uporabniski_profil_id=user).exists():
        return True
    return False

def list_visitations(request):
    print("LIST VISITATIONS")
    filter_form = FilterVisitationsForm()
    uporabnik = request.user

    #full_staff = User.objects.filer(is_staff=1)
    doctors_profiles = [ x.uporabniski_profil_id for x in Zdravnik.objects.all()]
    leaders_profiles = [ x.uporabniski_profil_id for x in Vodja_PS.objects.all()]
    doctors_leaders = doctors_profiles + leaders_profiles

    #filter_form.fields['filter_creator_id'].queryset=User.objects.filter(id__in=doctors_leaders)
    filter_form.fields['filter_creator_id'].queryset=Uporabnik.objects.filter(profil_id__in=doctors_leaders)

    izdajatelj = Uporabnik.objects.get(profil_id=uporabnik.id)
    if is_doctor(uporabnik):
        zdravnik=Zdravnik.objects.get(uporabniski_profil_id=uporabnik)
        delovni_nalogi = Delovni_nalog.objects.filter(zdravnik_id=zdravnik.sifra_zdravnika)
        filter_form.fields['filter_creator_id'].initial = izdajatelj
        filter_form.fields['filter_creator_id'].widget.attrs['disabled'] = 'disabled'
    elif is_leader_ps(uporabnik):
        print("IS LEADER")
        vodja=Vodja_PS.objects.get(uporabniski_profil_id=uporabnik)
        delovni_nalogi = Delovni_nalog.objects.all()
        filter_form.fields['filter_creator_id'].initial = izdajatelj
        nurse=Patronazna_sestra.objects.all()
    elif is_nurse(uporabnik):
        nurse=Patronazna_sestra.objects.get(uporabniski_profil_id=uporabnik)
        pacienti = Pacient.objects.filter(okolis_id=nurse.okolis_id)
        nalogi_vezani_na_pacienta=Pacient_DN.objects.filter(pacient_id__in=pacienti)
        delovni_nalogi = Delovni_nalog.objects.filter(id__in=[x.delovni_nalog_id for x in nalogi_vezani_na_pacienta])
        #filter_form.fields['filter_nurse_id']=nurse
        filter_form.fields['filter_nurse_id'].initial=str(nurse.sifra_patronazne_sestre)+" "+nurse.uporabniski_profil.first_name+" "+nurse.uporabniski_profil.last_name
        filter_form.fields['filter_creator_id'].widget.attrs['disabled'] = 'disabled'
        filter_form.fields['filter_nurse_id'].widget.attrs['disabled'] = 'disabled'
        #DODAJ FILTER
    else:
        print("ERROR!!")
        return

    form=FilterVisitationsForm(request.POST)
    if not form.is_valid():
        print("ERROR: FORM NOT VALID")

    print("PRE-POST")
    if request.POST:
        print(request.POST.get('filter_creator_id',0))
        if request.POST.get('filter_creator_id',0):
            print("filter_creator_id")
            uporabnik1=request.POST['filter_creator_id']
            print("UPORABNIK1: ",uporabnik1)
            profil=int(uporabnik1)#.profil_id
            print("PROFIL: ",profil)
            #ta filter mora biti na prvem mestu!!
            delovni_nalogi = Delovni_nalog.objects.all()
            if is_doctor(profil):
                creator = Zdravnik.objects.get(uporabniski_profil_id=profil)
                print("CREATOR: ",creator)
                delovni_nalogi = delovni_nalogi.filter(zdravnik_id=creator.sifra_zdravnika)
            elif is_leader_ps(request.POST['filter_creator_id']):
                creator = Vodja_PS.objects.get(uporabniski_profil_id=profil)
                print("Nalogi pred filtriranjem: ",delovni_nalogi)
                delovni_nalogi = delovni_nalogi.filter(vodja_PS_id=creator.sifra_vodje_PS)
                print("Nalogi po giltriranju: ",delovni_nalogi)
            filter_form.fields['filter_creator_id'].initial = request.POST['filter_creator_id']
        if request.POST.get('filter_date_from',0):
            print("filter date from")
            datum = datetime.strptime(request.POST['filter_date_from'], "%d.%m.%Y")
            delovni_nalogi = delovni_nalogi.filter(datum_prvega_obiska__gte=datum) #datetime.max
            #filter_form.fields['filter_date_from'] = request.POST['filter_date_from']
            filter_form.fields['filter_date_from'].initial = request.POST['filter_date_from']
        if request.POST.get('filter_date_to',0):
            print("filter date to")
            datum = datetime.strptime(request.POST['filter_date_to'], "%d.%m.%Y")
            #POPRAVEK, KER __lte ZACUDA NE VKLJUCUJE MEJE
            datum+=timedelta(days=1)

            delovni_nalogi = delovni_nalogi.filter(datum_prvega_obiska__lte=datum) #datetime.min
            #filter_form.fields['filter_date_to'] = request.POST['filter_date_to']
            filter_form.fields['filter_date_to'].initial = request.POST['filter_date_to']
        if request.POST.get('filter_visit_type',0):
            delovni_nalogi = delovni_nalogi.filter(vrsta_obiska_id=request.POST['filter_visit_type'])
            #filter_form.fields['filter_visit_type'] = request.POST['filter_visit_type']
            filter_form.fields['filter_visit_type'].initial=request.POST['filter_visit_type']
        if request.POST.get('filter_patient_id',0):
            pacientDN=Pacient_DN.objects.filter(pacient_id=request.POST['filter_patient_id'])
            nalogi_vezani_na_pacienta=[x.delovni_nalog_id for x in pacientDN]
            delovni_nalogi = delovni_nalogi.filter(id__in=nalogi_vezani_na_pacienta)
            #filter_form.fields['filter_patient_id'] = request.POST['filter_patient_id']
            filter_form.fields['filter_patient_id'].initial=request.POST['filter_patient_id']
        if request.POST.get('filter_nurse_id',0):
            nurse = Patronazna_sestra.objects.get(id=request.POST['filter_nurse_id'])
            pacienti = Pacient.objects.filter(okolis_id=nurse.okolis_id)
            nalogi_vezani_na_pacienta = Pacient_DN.objects.filter(pacient_id__in=pacienti)
            delovni_nalogi = delovni_nalogi.filter(id__in=[x.delovni_nalog_id for x in nalogi_vezani_na_pacienta])
            filter_form.fields['filter_nurse_id'].initial =  request.POST['filter_nurse_id']
        print("POST-POST")

    #  FORM QUERY SET
    # form.fields['adminuser'].queryset = User.objects.filter(account=accountid)
    visitations = Obisk.objects.all()
    material = Material_DN.objects.all()
    zdravila = Zdravilo_DN.objects.all()
    pacienti = Pacient_DN.objects.all()
    zdravniki = Zdravnik.objects.all()
    vodje_ps = Vodja_PS.objects.all()
    #delovni_nalogi = Delovni_nalog.objects.all()

    visitations=Obisk.objects.filter(delovni_nalog_id__in=delovni_nalogi)

    context = {'work_task_list':delovni_nalogi, 'visitations_list':visitations, 'nbar': 'v_visits', 'filter_form': filter_form, 'medications':zdravila, 'material': material, 'pacient_list': pacienti, 'doctors': zdravniki, 'head_nurses': vodje_ps}
    return render(request, 'visitations_list.html', context)

