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
from itertools import chain


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

    visitations = Obisk.objects.filter(p_sestra_id=nurse)
    nadomescanja = Nadomescanje.objects.filter(nadomestna_sestra_id=nurse, veljavno=True)
    obiski_n = []
    if len(nadomescanja) > 0:
        for nadomescanje in nadomescanja:
            nadomescani_obiski = Obisk.objects.filter(p_sestra_id=nadomescanje.sestra_id,
                                                      datum__gte=nadomescanje.datum_zacetek,
                                                      datum__lte=nadomescanje.datum_konec + timedelta(days=1))
            print("***Nadomescani obiski dodajam: ", nadomescani_obiski)
            if len(nadomescani_obiski) > 0:
                for x in nadomescani_obiski:
                    obiski_n.append(x)
                    # visitations = visitations.filter(id__in=obiski_n)
    else:
        print("***NADOMESCANJE PRAZEN QUERYSET")
    # obiski_n=obiski_n.filter(nadomestna_sestra_id=nurse)
    visitations = list(chain(visitations, obiski_n))
    visitations_today=[x for x in visitations if x.datum.date()==datetime.now().date()]
    visitations_yesterday = [x for x in visitations if x.datum.date() == (datetime.now()-timedelta(days=1)).date()]

    delovni_nalogi = Delovni_nalog.objects.all()
    material = Material_DN.objects.all()
    zdravila = Zdravilo_DN.objects.all()
    pacienti = Pacient_DN.objects.all()
    zdravniki = Zdravnik.objects.all()
    vodje_ps = Vodja_PS.objects.all()

    # V testne namene
    #obiski = Obisk.objects.all()
    #visitations_today = obiski
    #visitations_yesterday = obiski


    context = {'work_task_list':delovni_nalogi, 'visitations_list_today':visitations_today, 'visitations_list_yesterday':visitations_yesterday, 'nbar': 'v_nrs_visits_data', 'medications':zdravila, 'material': material, 'pacient_list': pacienti, 'doctors': zdravniki, 'head_nurses': vodje_ps}
    return render(request, 'visitations_nurse_data.html', context)





def edit_visitaiton_data(request):
    print("GOT IN VIA NEW FUNCTION !!!")

    # CREATE FORMS

    if('edit_visitation_data' in request.POST):
        visit_button_id = request.POST.get('edit_visitation_data')

        current_visit = Obisk.objects.get(id=visit_button_id)

        visitation_type = current_visit.obisk_vrsta_tostring()


        if(visitation_type == "Obisk otrocnice in novorojencka"):
            newBmotherForm = VisitNewbornAndMotherForm()
            context = {'nbar': 'v_nrs_visits_data', 'visitation_edit_id': visit_button_id, 'visitation_form': newBmotherForm }
            return render(request, 'visitations_nurse_editing.html', context)
            

        context = {'nbar': 'v_nrs_visits_data', 'visitation_edit_id': visit_button_id }
        return render(request, 'visitations_nurse_editing.html', context)

    # READ FORMS
    elif(request.POST):
        visitation_id = request.POST.get('submit_visitation_data', "")
        print("VISITATION ID FROM POST REQUEST: ", visitation_id)
        obisk=Obisk.objects.get(id=visitation_id)
        obisk_pacienti=[x.pacient_id for x in Pacient_DN.objects.filter(delovni_nalog_id=obisk.delovni_nalog_id)]
        polja=obisk.porocilo() #(x.polje_id,Meritev.objects.get(id=x.meritev_id).opis, x.id)
        polja_imena=["polje"+str(x[2]) for x in polja]
        #polja_meritve = Polje_meritev.objects.filter(id__in=meritve)

        if obisk.obisk_vrsta_tostring() == "Obisk otrocnice in novorojencka":
            form = VisitNewbornAndMotherForm(request.POST)
        elif obisk.obisk_vrsta_tostring() == "Obisk nosecnice":
            form = VisitNewbornAndMotherForm(request.POST)
        elif obisk.obisk_vrsta_tostring() == "Preventiva starostnika":
            form = VisitNewbornAndMotherForm(request.POST)
        elif obisk.obisk_vrsta_tostring() == "Aplikacija injekcij":
            form = VisitNewbornAndMotherForm(request.POST)
        elif obisk.obisk_vrsta_tostring() == "Odvzem krvi":
            form = VisitNewbornAndMotherForm(request.POST)
        elif obisk.obisk_vrsta_tostring() == "Kontrola zdravstvenega stanja":
            form = VisitNewbornAndMotherForm(request.POST)
        else:
            print("ERROR!! Neznan tip obiska!")
            return

        if not form.is_valid():
            print("ERROR: invalid form!!!!")

            # BASED ONF VISITATION ID, READ THE LINKED FORM

        # EXTRACT DATA FROM FORM
        for ime_polja in polja_imena:
            vrednost=form.cleaned_data[ime_polja]
            i=polja_imena.index(ime_polja)
            if not Porocilo_o_obisku.objects.filter(obisk_id=obisk.id, pacient_id=obisk_pacienti[0], polje_id=polja[i][0]).exists():
                porocilo_vnos = Porocilo_o_obisku(vrednost=vrednost, obisk_id=obisk.id, pacient_id=obisk_pacienti[0], polje_id=polja[i][0])
                porocilo_vnos.save()
            else:
                porocilo_vnos= Porocilo_o_obisku.objects.get(obisk_id=obisk.id, pacient_id=obisk_pacienti[0], polje_id=polja[i][0])
                porocilo_vnos.vrednost = vrednost
                porocilo_vnos.save()

        # SAVE DATA


        # REDIRECT TO PREVIOUS PAGE
        return redirect('link_visitations_nurse_data')





    