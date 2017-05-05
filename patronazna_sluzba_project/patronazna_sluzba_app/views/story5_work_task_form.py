# -*- coding: utf-8 -*-
# @login_required(login_url='/')
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.template.context_processors import csrf
from patronazna_sluzba_app.forms import *
from patronazna_sluzba_app.models import *
import datetime

# zdravila
def search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    # medicine = Zdravilo.objects.filter(ime__contains=search_text).distinct()[1:10]
    medicine = Zdravilo.objects.filter(kratko_poimenovanje__icontains=search_text)[:30]#values('ime').distinct().filter(ime__contains=search_text)[1:10]
    return render_to_response('ajax_search.html', {'medicine': medicine})


def search_patients(request):
    if request.method == 'POST':
        search_patient = request.POST['search_patient']
        added_patient = request.POST['added_patient']
        if added_patient =='':
            patients = Pacient.objects.filter(ime__contains=search_patient)
        else:
           # added_patient = added_patient[1:]
            print("imam stevilko skrbnika: ")
            print(int(added_patient))
            patients = Pacient.objects.filter(skrbnistvo_id=int(added_patient))
            print("REZULTAT POIZVEDBE: "+str(patients))

    else:
        search_patient = ''
        added_patient = ''
        patients = Pacient.objects.filter(ime__contains=search_patient)
     #all()  # filter
    return render_to_response('ajax_patient.html', {'patients': patients})

def visit_based_on_role(request):
    current_doc = None
    current_vodja_PS = None
    current_user = request.user
    try:
        current_doc = Zdravnik.objects.get(uporabniski_profil=current_user)
        ZS = current_doc.sifra_izvajalca_ZS
        print("DOC DELOVNI NALOG "+str(current_doc.sifra_zdravnika))
        user_role_type = 'Zdravnik'
    except:
        current_vodja_PS = Vodja_PS.objects.get(uporabniski_profil=current_user)
        ZS = current_vodja_PS.sifra_izvajalca_ZS
        print("VODJA PS DELOVNI NALOG ")
        user_role_type = 'Vodja'


    print('get request to visit role')
    if user_role_type == 'Vodja':
        visit_role = ['','Preventivni obisk']
    else:
        visit_role = ['', 'Preventivni obisk','Kurativni obisk']
    #for i in visit_role:
    #    print('Visit : '+i[0])
    #test='Preventivni obisk', 'Kurativni obisk';
    return render_to_response('ajax_visit_role.html',{'visit_role': visit_role})


def choose_visit_type(request):
    if request.method == 'POST':
        choose_visit = request.POST['choose_visit']

    else:
        choose_visit = 'Preventivni obisk'

    visits = Vrsta_obiska.objects.filter(tip=choose_visit)
    print('filter paremeter is: ' + choose_visit)
    return render_to_response('ajax_visit.html', {'visits': visits})

# bolezen
def illness_list_view(request):
    if request.method == 'POST':
        illness_list = request.POST['illness_list']
    else:
        illness_list = ''


    illness = Bolezen.objects.filter(ime__icontains=illness_list)
    return render_to_response('ajax_illness.html', {'illness': illness})

#vec patronaznih sester v istem okolišu
def health_visitor_view(request):
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        print("POST CALL")

    else:
        patient_id = '072044444444'
    print("The method is: "+request.method)
    patient = Pacient.objects.get(st_kartice=patient_id)#,flat=True)#Vrsta_obiska.objects.filter(tip=choose_visit)
    sisters = Patronazna_sestra.objects.filter(okolis_id=patient.okolis_id)
    print('Okolis pacienta: ' + str(patient.okolis_id))
    return render_to_response('ajax_health_visitor.html', {'sisters':sisters})

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
            delovni_nalog += 'Zavarovana oseba:\n'
            for i in pacient_list:
                print(i)
                delovni_nalog += '                ' + i + '\n'

        else:
            pacient = request.POST['searchPatient']
            delovni_nalog += 'Zavarovana oseba: ' + pacient + '\n'
            print('Pacient: ' + pacient)
        if podvrsta_vrsta_obiska == 'Aplikacija injekcij':
            izbranaZdravila = request.POST.getlist('cureId')

            delovni_nalog += 'Izbrana zdravila:\n'
            for i in izbranaZdravila:
                print("Zdravilo " + i)
                delovni_nalog += '          ' + i + '\n'
        elif podvrsta_vrsta_obiska == 'Odvzem krvi':
            print("odvzem krvi")

            delovni_nalog += 'Material:\n'
            izbran_material = request.POST.getlist('materialDN')
            for i in izbran_material:
                print('material: ' + i)
                delovni_nalog += '          ' + i + '\n'

        delovni_nalog += 'Datum prvega obiska: '+prvi_obisk+'\nObveznost obiska: '+obveznost+'\nStevilo obiskov: '+stevilo_obiskov+'\n'
        #zdravilo = request.POST['medicine']
        #autoData = request.POST['searchPatient']
        #pacient = autoData.split()

        #   =====================>>>>>>==============<<<<<<<========================
        #   ===========================   BACK BACK  ===============================
        #   =====================>>>>>>==============<<<<<<<========================

        #   Adding doctor and leader of PS
        current_doc = None
        current_vodja_PS = None
        current_user = request.user
        creator_id = None
        try:
            current_doc = Zdravnik.objects.get(uporabniski_profil=current_user)
            ZS = current_doc.sifra_izvajalca_ZS
            print("DOC DELOVNI NALOG")

        except:
            current_vodja_PS = Vodja_PS.objects.get(uporabniski_profil=current_user)
            ZS = current_vodja_PS.sifra_izvajalca_ZS
            print("VODJA PS DELOVNI NALOG")


        #   Adding time frames
        cas_obisk = 0
        obisk_tip = "Obdobje"
        if casovni_interval == 0:
            cas_obisk = casovno_obdobje
        elif casovno_obdobje == 0:
            obisk_tip = "Interval"
            cas_obisk = casovni_interval
        else:
            print("wtf is happening?")

        sep = ' '
        bolezen_id = request.POST['search_illness'].split(sep, 1)[0]
        print("BOLEZEN", bolezen_id)
        bolezen = Bolezen.objects.get(sifra=bolezen_id)


        #   Create work task form
        work_task_f = Delovni_nalog(st_obiskov=stevilo_obiskov, vrsta_obiska=visity_type,
                                    zdravnik=current_doc, datum_prvega_obiska=first_visit_date,
                                    cas_obiskov_dolzina=cas_obisk, izvajalec_zs=ZS,
                                    vodja_PS=current_vodja_PS, cas_obiskov_tip=obisk_tip, bolezen=bolezen)
        work_task_f.save()

        print("work tast form saved")

        #   PATIENT====================================================================

        #   Add more patients
        if podvrsta_vrsta_obiska == "Obisk otrocnice" or podvrsta_vrsta_obiska == 'Obisk novorojencka':
            print("obisk otrocnice")
            pacient_list = request.POST.getlist('addPatient')

            main_patient = Pacient.objects.get(st_kartice=pacient_list[0][0:12])
            print("main patient", main_patient.ime)
            for i in pacient_list:
                card_list = i[0:12]
                print("card", card_list)
                patient = Pacient.objects.get(st_kartice=card_list)
                patient_wtf = Pacient_DN(delovni_nalog=work_task_f, pacient=patient)
                patient_wtf.save()
                print("Shranjen pacient in delovni nalog")
            #dobi ven paciente
        #   Add one patient
        else:
            print("printam pacienta card number", pacient[0:12])
            patient_card_number = pacient[0:12]

            patient = Pacient.objects.get(st_kartice=patient_card_number)
            main_patient = patient
            patient_wtf = Pacient_DN(delovni_nalog=work_task_f, pacient=patient)
            patient_wtf.save()
            print("work task form link to  patient saved")

            if podvrsta_vrsta_obiska == 'Odvzem krvi':
                print("odvzem krvi")

                izbran_material = request.POST.getlist('materialDN')
                for i in izbran_material:
                    quantity = int(i[-1:])
                    sep = ' '
                    material_name = i.split(sep, 1)[0]
                    print(quantity)
                    print(material_name)
                    mat = Material.objects.get(ime=material_name)
                    material_wtf = Material_DN(material=mat, delovni_nalog=work_task_f, kolicina=quantity)
                    material_wtf.save()
                    print("Shranjen material", quantity, ",", material_name)
            elif podvrsta_vrsta_obiska == 'Aplikacija injekcij':
                for i in izbranaZdravila:
                    sickness = Zdravilo.objects.get(kratko_poimenovanje=i)

                    zdr = Zdravilo_DN(zdravilo=sickness, delovni_nalog=work_task_f)
                    zdr.save()
                #return HttpResponse("Uspesno kreiranje delovnega naloga "+delovni_nalog);
                return render(request, 'task_creation_success.html')



        # VISITS====================================================================
        interval_period = int(cas_obisk)
        type = obisk_tip
        number_of_visits = int(stevilo_obiskov)
        date_current = datetime.datetime.strptime(first_visit_date, "%Y-%m-%d")

        # if we have interval type of visitation
        if type == 'Interval':
            for i in range(int(number_of_visits)):
                date_next = date_current + datetime.timedelta(days=int(interval_period))
                weekno = date_next.weekday()
                if weekno == 6 or weekno == 0:
                    date_next = date_next + datetime.timedelta(days=2)
                    weekno = date_next.weekday()

                p_sestra = Patronazna_sestra.objects.get(sifra_patronazne_sestre=request.POST['nurse_id'])
                obv = 0
                if obveznost == "Obvezen":
                    obv = 1
                    obveznost = "Okviren"

                visit = Obisk(delovni_nalog=work_task_f, datum=date_current, p_sestra=p_sestra, obvezen_obisk=obv)
                visit.save()
                date_current = date_next
                print("Obisk shranjen (INTERVAL); datum: ", date_current)
        else:
            # space = number of days so that visits are the most balanced throughout the period
            space = int(interval_period / number_of_visits)
            for i in range(int(number_of_visits)):
                #   If there are 1 or more days between visits
                if int(interval_period) >= int(number_of_visits):
                    date_next = date_current + datetime.timedelta(days=int(space))
                    #   check if its weekend
                    weekno = date_next.weekday()

                    if weekno == 6 or weekno == 0:
                        date_next = date_next + datetime.timedelta(days=2)
                        weekno = date_next.weekday()

                    # find the appropriate nurse for the county
                    p_sestra = Patronazna_sestra.objects.get(sifra_patronazne_sestre=request.POST['nurse_id'])

                    print("p_sestra", p_sestra)
                    #   check if the first visit is mandatory on that day
                    obv = 0
                    if obveznost == "Obvezen":
                        obv = 1
                        obveznost = "Okviren"

                    visit = Obisk(delovni_nalog=work_task_f, datum=date_current, p_sestra=p_sestra,
                                  obvezen_obisk=obv)
                    visit.save()
                    date_current = date_next
                    print("Obisk shranjen (OBDOBJE); datum: ", date_current)
                else:
                    return render(request, 'task_creation_success.html')
                    #return HttpResponse(
                    #   "Uspesno kreiranje delovnega naloga AMPAK NISO DODANI OBISKI KER JE PREKRATKO OBDOBJE" + delovni_nalog);

        #return HttpResponse("Uspesno kreiranje delovnega naloga "+delovni_nalog);

        return render(request, 'task_creation_success.html')



    else:
        current_doc = None
        current_vodja_PS = None
        current_user = request.user
        creator_id = None
        try:
            current_doc = Zdravnik.objects.get(uporabniski_profil=current_user)
            print("DOCTOR " + str(current_doc.sifra_zdravnika))
            creator_id = current_doc.sifra_zdravnika
        except:
            current_vodja_PS = Vodja_PS.objects.get(uporabniski_profil=current_user)
            ZS = current_vodja_PS.sifra_izvajalca_ZS
            print("VODJA  ")
            creator_id = current_vodja_PS.sifra_vodje_PS

        args = {}
        args.update(csrf(request))

        args['medicine'] = Zdravilo.objects.all()
        args['work_task_form'] = WorkTaskForm()
        args['creator_id'] = creator_id
        # form = WorkTaskForm()

    return render(request, 'work_task.html', args)
