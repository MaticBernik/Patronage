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
# from patronazna_sluzba_app.forms import AddNursingPatientForm, ChangePasswordForm, LoginForm, PatientRegistrationFrom, RegisterMedicalStaffForm, WorkTaskForm, FilterVisitationsForm
# from patronazna_sluzba_app.models import Izvajalec_ZS, Pacient, Patronazna_sestra, Sodelavec_ZD, User, Vodja_PS, Zdravnik, Obisk, Delovni_nalog, Pacient_DN, Material_DN, Zdravilo_DN, Uporabnik, Nadomescanje
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
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

def list_active_visitations(request):
    uporabnik = request.user
    nurse=None
    if is_nurse(uporabnik):
        nurse=Patronazna_sestra.objects.get(uporabniski_profil_id=uporabnik)
    else:
        print("ERROR!!")
        return
    nadomescaneSestre=[x.sestra_id for x in Nadomescanje.objects.filter(nadomestna_sestra_id=nurse, veljavno=True)]
    print("***Nadomescane sestre: ",nadomescaneSestre)
    nadomescaneSestre.append(nurse)
    #pacienti = Pacient.objects.filter(okolis_id__in=[x.okolis_id for x in sestre])
    #nalogi_vezani_na_pacienta = Pacient_DN.objects.filter(pacient_id__in=pacienti)
    #delovni_nalogi = Delovni_nalog.objects.filter(id__in=[x.delovni_nalog_id for x in nalogi_vezani_na_pacienta])
    print("***sestre",nadomescaneSestre)
    obiski = Obisk.objects.filter(p_sestra_id__in=nadomescaneSestre)
    print("***danes: ",datetime.now().date())
    visitations_today=obiski.filter(datum=datetime.now().date())
    visitations_yesterday=obiski.filter(datum=(datetime.now()-timedelta(days=1)).date())

    delovni_nalogi = Delovni_nalog.objects.all()
    material = Material_DN.objects.all()
    zdravila = Zdravilo_DN.objects.all()
    pacienti = Pacient_DN.objects.all()
    zdravniki = Zdravnik.objects.all()
    vodje_ps = Vodja_PS.objects.all()

    # V testne namene
    obiski = Obisk.objects.all()
    visitations_today = obiski
    visitations_yesterday = obiski


    context = {'work_task_list':delovni_nalogi, 'visitations_list_today':visitations_today, 'visitations_list_yesterday':visitations_yesterday, 'nbar': 'v_nrs_visits_data', 'medications':zdravila, 'material': material, 'pacient_list': pacienti, 'doctors': zdravniki, 'head_nurses': vodje_ps}
    return render(request, 'visitations_nurse_data.html', context)





def edit_visitaiton_data(request):
    print("GOT IN VIA NEW FUNCTION !!!")


    if('edit_visitation_data' in request.POST):
        visit_button_id = request.POST.get('edit_visitation_data')

        current_visit = Obisk.objects.get(id=visit_button_id)

        visitation_type = current_visit.obisk_vrsta_tostring()

        seznam_polj = current_visit.porocilo()
        details_list = [ detail for (_,detail,_) in seznam_polj]
        print()
        print("SEZNAM OPISOV")
        print(details_list)
        print()
        # clean the list
        prev_string = details_list[0]
        for i in range(0, len(details_list)):
            current_string = details_list[i]
            if(i != 0 and prev_string == current_string):
                details_list[i] = ""
            prev_string = current_string

        print()
        print("NOV SEZNAM OPISOV")
        print(details_list)
        print()

        if(visitation_type == "Obisk otrocnice in novorojencka"):
            newBmotherForm = VisitNewbornAndMotherForm()
            context = {'nbar': 'v_nrs_visits_data', 'visitation_edit_id': visit_button_id, 'visitation_form': newBmotherForm }
            return render(request, 'visitations_nurse_editing.html', context)



        context = {'nbar': 'v_nrs_visits_data', 'visitation_edit_id': visit_button_id }
        return render(request, 'visitations_nurse_editing.html', context)



    