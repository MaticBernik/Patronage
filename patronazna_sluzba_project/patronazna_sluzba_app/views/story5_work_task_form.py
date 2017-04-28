# -*- coding: utf-8 -*-
# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
from django.template import Context, loader, RequestContext


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


def fix_date(date_of_visit):
    dd = date_of_visit[0:2]
    mm = date_of_visit[3:5]
    yyyy = date_of_visit[6:10]
    print(dd, " ", mm, " ", yyyy)
    dat = yyyy + '-' + mm + '-' + dd

    return dat


def return_doc():

    return


def return_vodja_PS():

    return

def return_patient():

    return

def work_task_view(request):

    if request.method == 'POST':
        form = WorkTaskForm(request.POST)

        vrsta_obiska = request.POST['visitType']
        podvrsta_vrsta_obiska = request.POST['visitTypeDetail']
        prvi_obisk = request.POST['visitDate']

        visity_type = Vrsta_obiska.objects.get(ime=podvrsta_vrsta_obiska)
        first_visit_date = fix_date(prvi_obisk)

        try:
            if request.POST['mandatory']:
                obveznost = 'Obvezen'
        except:
            obveznost = 'Okviren'
        stevilo_obiskov = request.POST['visitCount']

        delovni_nalog = "Tip obiska: "+vrsta_obiska+"\nVrsta obiska details: "+podvrsta_vrsta_obiska+'\n'

        casovni_interval = 0
        casovno_obdobje = 0
        try:
            casovni_interval = request.POST['timeInterval']
        except:
            casovno_obdobje = request.POST['timePeriod']

        if podvrsta_vrsta_obiska == "Obisk otrocnice" or podvrsta_vrsta_obiska == 'Obisk novorojencka':
            print("obisk otrocnice")
            pacient_list = request.POST.getlist('addPatient')
            delovni_nalog+='Zavarovana oseba:\n'
            for i in pacient_list:
                print(i)
                delovni_nalog += '                '+i+'\n'

        else:
            pacient = request.POST['searchPatient']
            delovni_nalog += 'Zavarovana oseba: '+ pacient+'\n'
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

        #   =====================>>>>>>==============<<<<<<<========================
        #   ===========================   BACK BACK  ===============================
        #   =====================>>>>>>==============<<<<<<<========================

        #   Adding material if or meds if needed
        if podvrsta_vrsta_obiska == 'Aplikacija injekcij':
            print("aplikacija injekcij")
            izbranaZdravila
        elif podvrsta_vrsta_obiska == 'Odvzem krvi':
            print("odvzem krvi")
            izbran_material

        #   Adding doctor and leader of PS
        current_doc = None
        current_vodja_PS = None
        current_user = request.user
        try:
            us = User.objects.get(email='joze.dolenc@mail.si')
            current_doc = Zdravnik.objects.get(uporabniski_profil=us)
            print("hardcodan doc")

            #current_doc = Zdravnik.objects.get(uporabniski_profil=current_user)
            ZS = current_doc.sifra_izvajalca_ZS
        except:
            current_vodja_PS = Vodja_PS.objects.get(uporabniski_profil=current_user)
            ZS = current_vodja_PS.sifra_izvajalca_ZS


        #   Adding time frames
        cas_obisk = 0
        obisk_tip = "Interval"
        if casovni_interval == 0:
            cas_obisk = casovno_obdobje
        elif casovno_obdobje == 0:
            obisk_tip = "Obdobje"
            cas_obisk = casovni_interval
        else:
            print("wtf is happening?")


        #   Create work task form
        work_task_f = Delovni_nalog(st_obiskov=stevilo_obiskov, vrsta_obiska=visity_type,
                                    zdravnik=current_doc, datum_prvega_obiska=first_visit_date,
                                    cas_obiskov_dolzina=cas_obisk, izvajalec_zs=ZS,
                                    vodja_PS=current_vodja_PS, cas_obiskov_tip=obisk_tip, obveznost_obiska=obveznost)
        work_task_f.save()

        print("work tast form saved")


        #   PATIENT====================================================================

        #   Add more patients
        if podvrsta_vrsta_obiska == "Obisk otrocnice" or podvrsta_vrsta_obiska == 'Obisk novorojencka':
            print("obisk otrocnice")
            #dobi ven paciente
        #   Add one patient
        else:
            print("printam pacienta card number", pacient[0:12])
            patient_card_number = int(pacient[0:12])

            patient = Pacient.objects.get(st_kartice=patient_card_number)
            patient_wtf = Pacient_DN(delovni_nalog=work_task_f, pacient=patient)
            patient_wtf.save()
            print("work task form link to  patient saved")

        return HttpResponse("Uspesno kreiranje delovnega naloga "+delovni_nalog);



    else:
        args = {}
        args.update(csrf(request))

        args['medicine'] = Zdravilo.objects.all()
        args['work_task_form'] = WorkTaskForm()
        #form = WorkTaskForm()

    return render(request, 'work_task.html', args)
