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

POLJA_UNIKATNI_VNOSI=['Porodna teža otroka (g)','Porodna višina otroka (cm)','Datum rojstva otroka']


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
    print("!!!!!!!!!VISITATIONS - pred delitvijo: ",visitations)
    for x in visitations:
        print(x.datum)
    visitations_today=[x for x in visitations if x.datum.date()==datetime.now().date()]
    visitations_yesterday = [x for x in visitations if x.datum.date() == (datetime.now()-timedelta(days=1)).date()]
    print("!!!!!!!!!!!VISITATIONS_TODAY: ",visitations_today)
    print("!!!!!!!!!!!VISITATIONS_YESTERDAY: ",visitations_yesterday)

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
    
    vsa_nadomescanja = Nadomescanje.objects.all()
    vsa_porocila = Porocilo_o_obisku.objects.all()
    vsa_polja_meritev = Polje_meritev.objects.all()
    vsa_pacient_DN = Pacient_DN.objects.all()

    context = {'work_task_list':delovni_nalogi, 'visitations_list_today':visitations_today, 'visitations_list_yesterday':visitations_yesterday, 'nbar': 'v_nrs_visits_data', 'medications':zdravila, 'material': material, 'pacient_list': pacienti, 'doctors': zdravniki, 'head_nurses': vodje_ps, 'substitutions': vsa_nadomescanja, 'all_visit_reports': vsa_porocila, 'all_measure_fields': vsa_polja_meritev, 'all_p_DN': vsa_pacient_DN}
    return render(request, 'visitations_nurse_data.html', context)





def edit_visitaiton_data(request):
    #change_visitation_date boolean field
    print("GOT IN VIA NEW FUNCTION !!!")

    # CREATE FORMS

    if('edit_visitation_data' in request.POST):
        visit_button_id = request.POST.get('edit_visitation_data')

        current_visit = Obisk.objects.get(id=visit_button_id)

        visitation_type = current_visit.obisk_vrsta_tostring()

        input_data_form = InputVisitationDataForm(request.POST,v_type=visitation_type, visit=current_visit)

        current_worktask = Delovni_nalog.objects.get(id=current_visit.delovni_nalog_id)
        pacienti_obiska = Pacient_DN.objects.filter(delovni_nalog=current_worktask)

        context = {'nbar': 'v_nrs_visits_data', 'visitation_edit_id': visit_button_id, 'visitation_form': input_data_form, 'visitation_patients': pacienti_obiska, 'type_of_visit': visitation_type }
        return render(request, 'visitations_nurse_editing.html', context)
            


    # READ FORMS
    elif(request.POST):
        visitation_id = request.POST.get('submit_visitation_data', "")
        obisk=Obisk.objects.get(id=visitation_id)
        obisk_pacienti=[x.pacient_id for x in Pacient_DN.objects.filter(delovni_nalog_id=obisk.delovni_nalog_id)]
        polja=obisk.porocilo() #(x.polje_id,Meritev.objects.get(id=x.meritev_id).opis, x.id)
        polja_tmp=[]
        polja_imena_tmp=["polje"+str(x[2]) for x in polja]
        polja_imena=[]
        for ime in polja_imena_tmp:
            for pacient_id in obisk_pacienti:
                polja_imena.append(ime+"_"+str(pacient_id))
        #polja_meritve = Polje_meritev.objects.filter(id__in=meritve)

        for polje in polja:
            polja_tmp.append(polje)
            polja_tmp.append(polje)
        polja=polja_tmp

        if obisk.obisk_vrsta_tostring() == "Obisk otrocnice in novorojencka":
            #form = InputVisitationDataForm(request.POST)
            form = InputVisitationDataForm(request.POST, v_type=obisk.obisk_vrsta_tostring(), visit=obisk)
            if len(obisk_pacienti)<2:
                print("S tem obiskom nekaj ni vredu! Obisk otrocnice in novorojencka bi moral imeti pripisana 2 pacienta")

            #nalogi_pacient_1 = [x.delovni_nalog_id for x in Pacient_DN.objects.filter(pacient_id=obisk_pacienti[0])]
            #obiski_pacient_1 = Obisk.objects.filter(delovni_nalog_id__in=nalogi_pacient_1)
            polja_porocila_pacient_1 = Polje_v_porocilu.objects.filter(id__in=[x.polje_id for x in Porocilo_o_obisku.objects.filter(pacient_id=obisk_pacienti[0])])
            for polje in polja_porocila_pacient_1:
                if polje.ime in POLJA_UNIKATNI_VNOSI:
                    print("Polje ",polje.ime," v formi bi moralo biti zaklenjeno, saj je ze bilo vneseno pri enem od predhodnjih meritev (meri pa se samo enkrat)")

            #Sedaj nepotrebno, saj dobim informacijo iz id-ja polja
            '''# Doloci, ali polje pripada otrocnici ali novorojencku:
            pacient_polje=[]
            for polje in polja:
                pripadajoce_meritve=Meritev.objects.filter(opis=polje[1], id__in=[x.meritev_id for x in Polje_meritev.objects.filter(polje_id=polje[0])])
                pripadajoce_vrste_obiskov = [x.vrsta_obiska_id for x in pripadajoce_meritve]
                pripadajoce_sifre_meritev=[x.sifra for x in pripadajoce_meritve]

                # 1. VARIANTA
                #if len(pripadajoce_vrste_obiskov)==0:
                #    print("NAPAKA! Polje gotovo pripada vsaj eni vrsti obiska.")
                #if 30 in pripadajoce_vrste_obiskov:
                #    print("To polje se nanasa na NOVOROJENCKA!")
                #elif 80 in pripadajoce_vrste_obiskov:
                #    print("To polje se nanasa na OTROCNICO!")

                #2.VARIANTA
                if len(pripadajoce_sifre_meritev) == 0:
                    print("NAPAKA! Polje gotovo pripada vsaj eni vrsti obiska.")

                for i in range(len(pripadajoce_sifre_meritev)):
                    sifra = pripadajoce_sifre_meritev[i]
                    if pripadajoce_vrste_obiskov[i]==20:
                        if sifra >=10 and sifra <=240:
                            print("To polje se nanasa na OTROCNICO!")
                            pacient_polje.append("OTROCNICA")
                        elif sifra >=250 and sifra <=380:
                            print("To polje se nanasa na NOVOROJENCKA!")
                            pacient_polje.append("NOVOROJENCEK")'''

        elif obisk.obisk_vrsta_tostring() == "Obisk nosecnice":
            form = InputVisitationDataForm(request.POST, v_type=obisk.obisk_vrsta_tostring(), visit=obisk)
        elif obisk.obisk_vrsta_tostring() == "Preventiva starostnika":
            form = InputVisitationDataForm(request.POST, v_type=obisk.obisk_vrsta_tostring(), visit=obisk)
        elif obisk.obisk_vrsta_tostring() == "Aplikacija injekcij":
            form = InputVisitationDataForm(request.POST, v_type=obisk.obisk_vrsta_tostring(), visit=obisk)
        elif obisk.obisk_vrsta_tostring() == "Odvzem krvi":
            form = InputVisitationDataForm(request.POST, v_type=obisk.obisk_vrsta_tostring(), visit=obisk)
        elif obisk.obisk_vrsta_tostring() == "Kontrola zdravstvenega stanja":
            form = InputVisitationDataForm(request.POST, v_type=obisk.obisk_vrsta_tostring(), visit=obisk)
        else:
            print("ERROR!! Neznan tip obiska!")
            return

        if not form.is_valid():
            print("ERROR: invalid form!!!!")


        # EXTRACT DATA FROM FORM
        for ime_polja in polja_imena:
            if not request.POST.get(ime_polja,0):
                continue
            id_pacienta=ime_polja[ime_polja.index('_')+1:]
            vrednost=form.cleaned_data[ime_polja]
            i=polja_imena.index(ime_polja)
            print("ID OBISKA",obisk.id)
            if not Porocilo_o_obisku.objects.filter(obisk_id=obisk.id, pacient_id=id_pacienta, polje_id=polja[i][0]).exists():
                if not datetime.now().date() == obisk.datum.date():
                    print("Datum vnosa porocila je razlicen od datuma obiska ---> potrebna potrditev dejanskega datuma obiska")

                porocilo_vnos = Porocilo_o_obisku(vrednost=vrednost, obisk_id=obisk.id, pacient_id=id_pacienta, polje_id=polja[i][0])
                porocilo_vnos.save()
            else:
                porocilo_vnos= Porocilo_o_obisku.objects.get(obisk_id=obisk.id, pacient_id=id_pacienta, polje_id=polja[i][0])
                porocilo_vnos.vrednost = vrednost
                porocilo_vnos.save()

        # SAVE DATA
        if request.POST.get('change_visitation_date',0):
            popravi_datum=request.POST['change_visitation_date']
            print("!!!!!!!!POPRAVI DATUM: ",popravi_datum)
            if popravi_datum=='on':
                obisk.datum=datetime.now()
                obisk.save()


        # REDIRECT TO PREVIOUS PAGE
        return redirect('link_visitations_nurse_data')





    