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

    #visitations = Obisk.objects.filter(p_sestra_id=nurse)
    #planned_today = Plan.objects.filter(datum__icontains=datetime.now().date()).values_list('planirani_obisk_id',flat=True)
    planned_today= Plan.objects.filter(datum__gte=datetime.now().date(), datum__lte=(datetime.now()+timedelta(days=1)))
    print("PLANNED TODAY")
    print(planned_today)
    print("DATE FILTER")
    print(datetime.now().date())
    #planned_yesterday = Plan.objects.filter(datum__icontains=(datetime.now().date()-timedelta(days=1)).date()).values_list('planirani_obisk_id', flat=True)
    planned_yesterday= Plan.objects.filter(datum__gte=datetime.now().date() - timedelta(days=1), datum__lte=(datetime.now().date()))
    planned_yesterday = Plan.objects.filter(datum = datetime.now().date()-timedelta(days=1))
    print(planned_today)
    print(planned_yesterday)
    visitations = Obisk.objects.filter(p_sestra_id=nurse,n_sestra_id=None)
    #visitations |= Obisk.objects.filter(n_sestra_id=nurse)
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
    #print("!!!!!!!!!VISITATIONS - pred delitvijo: ",visitations)
    for x in visitations:
        print(x.datum)
    #visitations_today=[x for x in visitations if x.datum.date()==datetime.now().date()]
    visitations_today=[x for x in visitations if x.id in [x.planirani_obisk_id for x in planned_today]]

    #visitations_yesterday = [x for x in visitations if x.datum.date() == (datetime.now().date()-timedelta(days=1)).date()]
    visitations_yesterday = [x for x in visitations if x.id in [x.planirani_obisk_id for x in planned_yesterday]]
    #print("!!!!!!!!!!!VISITATIONS_TODAY: ",visitations_today)
    #print("!!!!!!!!!!!VISITATIONS_YESTERDAY: ",visitations_yesterday)

    delovni_nalogi = Delovni_nalog.objects.all()
    material = Material_DN.objects.all()
    zdravila = Zdravilo_DN.objects.all()
    pacienti = Pacient_DN.objects.all()
    zdravniki = Zdravnik.objects.all()
    vodje_ps = Vodja_PS.objects.all()

    # V testne namene
    # obiski = Obisk.objects.all()
    # visitations_today = obiski
    # visitations_yesterday = obiski[:10]
    
    vsa_nadomescanja = Nadomescanje.objects.all()
    vsa_porocila = Porocilo_o_obisku.objects.all()
    vsa_polja_meritev = Polje_meritev.objects.all()
    vsa_pacient_DN = Pacient_DN.objects.all()


    ## TEST AREA VISIT_REPORT_WITH ALL THE DATA
    '''print()
    print("                     POROCILO                         ")
    print(" ==================================================== ")
    for i in obiski[0].porocilo_izpis():
        print(i)'''



    context = {'work_task_list':delovni_nalogi, 'visitations_list_today':visitations_today, 'visitations_list_yesterday':visitations_yesterday, 'nbar': 'v_nrs_visits_data', 'medications':zdravila, 'material': material, 'pacient_list': pacienti, 'doctors': zdravniki, 'head_nurses': vodje_ps, 'substitutions': vsa_nadomescanja, 'all_visit_reports': vsa_porocila, 'all_measure_fields': vsa_polja_meritev, 'all_p_DN': vsa_pacient_DN}
    return render(request, 'visitations_nurse_data.html', context)





def edit_visitaiton_data(request):
    #change_visitation_date boolean field
    # print("GOT IN VIA NEW FUNCTION !!!")

    # CREATE FORMS

    if('edit_visitation_data' in request.POST):
        print(" POST - edit_visitation_data ")
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
        print(" POST - FORM SUBMITTION ")
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
            for i in range(len(obisk_pacienti)):
                polja_tmp.append(polje)
        polja=polja_tmp

        if obisk.obisk_vrsta_tostring() == "Obisk otrocnice in novorojencka":
            #form = InputVisitationDataForm(request.POST)
            form = InputVisitationDataForm(request.POST, v_type=obisk.obisk_vrsta_tostring(), visit=obisk)
            if len(obisk_pacienti)<2:
                print("S tem obiskom nekaj ni vredu! Obisk otrocnice in novorojencka bi moral imeti pripisana 2 pacienta")

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
        obisk_opravljen=False
        for ime_polja in polja_imena:
            if not request.POST.get(ime_polja,0):
                continue
            obisk_opravljen=True
            id_pacienta=ime_polja[ime_polja.index('_')+1:]
            # vrednost=form.cleaned_data[ime_polja]
            vrednost = request.POST.get(ime_polja)
            i=polja_imena.index(ime_polja)
            # print("ID OBISKA",obisk.id)
            if not Porocilo_o_obisku.objects.filter(obisk_id=obisk.id, pacient_id=id_pacienta, polje_id=polja[i][0], meritev=polja[i][3]).exists():
                '''if not datetime.now().date() == obisk.datum.date():
                    print("Datum vnosa porocila je razlicen od datuma obiska ---> potrebna potrditev dejanskega datuma obiska")'''

                porocilo_vnos = Porocilo_o_obisku(vrednost=vrednost, obisk_id=obisk.id, pacient_id=id_pacienta, polje_id=polja[i][0], meritev_id=polja[i][3])
                porocilo_vnos.save()
            else:
                porocilo_vnos= Porocilo_o_obisku.objects.get(obisk_id=obisk.id, pacient_id=id_pacienta, polje_id=polja[i][0],  meritev=polja[i][3])
                porocilo_vnos.vrednost = vrednost
                porocilo_vnos.save()

        if obisk_opravljen and not obisk.opravljen:
            obisk.opravljen=True
            obisk.save()

        # SAVE DATA
        if request.POST.get('change_visitation_date',0):
            popravi_datum=request.POST['change_visitation_date']
            # print("!!!!!!!!POPRAVI DATUM: ",popravi_datum)
            if popravi_datum=='on':
                obisk.datum=datetime.now().date()
                obisk.save()

        #POPRAVI KOLICINE UPORABLJENEGA MATERIALA IN ZDRAVIL
        obisk_material=Material_Obisk.objects.filter(obisk_id=obisk)
        obisk_zdravila=Zdravilo_Obisk.objects.filter(obisk_id=obisk)

        imena_polj_material=[]
        imena_polj_zdravila=[]
        for m in obisk_material:
            imena_polj_material.append("polje"+str(obisk.id)+'_material_'+str(m.material_id))
        for z in obisk_zdravila:
            imena_polj_zdravila.append("polje"+str(obisk.id)+'_zdravilo_'+str(z.nacionalna_sifra))

        print("imena polj zdravila: ", imena_polj_zdravila)
        print("imena polj material: ",imena_polj_material)

        for polje in imena_polj_material:
            if not request.POST.get(polje, 0):
                print("Napaka! polje ne obstaja!")
                continue
            vrednost = request.POST.get(polje)
            material_id=int(polje[polje.index('_material_')+len('_material_'):])
            vnos_v_bazi = Material_Obisk.objects.filter(obisk_id=obisk, material_id=material_id)
            vnos_v_bazi=vnos_v_bazi[0]
            if vrednost != vnos_v_bazi.kolicina:
                vnos_v_bazi.kolicina=vrednost
                vnos_v_bazi.save()

        for polje in imena_polj_zdravila:
            if not request.POST.get(polje, 0):
                print("Napaka! polje ne obstaja!")
                continue
            vrednost = request.POST.get(polje)
            zdravilo_id = int(polje[polje.index('_zdravilo_') + len('_zdravilo_'):])
            vnos_v_bazi = Zdravilo_Obisk.objects.filter(obisk_id=obisk, zdravilo_id_id=zdravilo_id)
            vnos_v_bazi = vnos_v_bazi[0]
            if vrednost != vnos_v_bazi.kolicina:
                vnos_v_bazi.kolicina = vrednost
                vnos_v_bazi.save()

        # REDIRECT TO PREVIOUS PAGE
        return redirect('link_visitations_nurse_data')





    