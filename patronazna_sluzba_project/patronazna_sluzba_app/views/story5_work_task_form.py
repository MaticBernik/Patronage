# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf


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

def work_task_view(request):

    if request.method == 'POST':
        form = WorkTaskForm(request.POST)

        vrsta_obiska = request.POST['visitType']
        podvrsta_vrsta_obiska = request.POST['visitTypeDetail']


        prvi_obisk = request.POST['visitDate']

        try:
            if request.POST['mandatory']:
                obveznost = 'Obvezen'
        except:
            obveznost = 'Okviren'
        stevilo_obiskov = request.POST['visitCount']

        delovni_nalog = "Tip obiska: "+vrsta_obiska+"\nVrsta obiska details: "+podvrsta_vrsta_obiska+'\n'
        try:
            casovni_interval = request.POST['timeInterval']
        except:
            casovno_obdobje = request.POST['timePeriod']
        """
        if casovni_interval != '':
            print("casovni interval")
        else:
            casovno_obdobje = request.POST['timePeriod']
        """

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
        #   Add doctor for this worktask form
        current_user = request.user
        try:
            current_doc = Zdravnik.objects.get(uporabniski_profil=current_user)
        except:
            us = User.objects.get(email='zd@gmail.com')
            current_doc = Zdravnik.objects.get(uporabniski_profil=us)
            print("hardcodan doc")

            #return HttpResponse("Can't find this doctor(user) in the database")

        #nurse_id = form.cleaned_data['nurse_id']

        try:
            #current_nurse = Patronazna_sestra.objects.get(sifra_patronazne_sestre=nurse_id)
            current_nurse = Patronazna_sestra.objects.get(sifra_patronazne_sestre=12121)
        except:
            print("hardcodam sestro kr se nimamo user vlog naretih")
            current_nurse = Patronazna_sestra.objects.get(sifra_patronazne_sestre='99998')

            # anita.gorenc@mail.si
            #return HttpResponse("Can't find current nurse")
        #ZS = current_doc.sifra_izvajalca_ZS

        print("printam pacienta card number", pacient[0:12])
        patient_card_number = int(pacient[0:12])

        try:
            patient = Pacient.objects.get(st_kartice=patient_card_number)
            print("patient found")
        except:
            return HttpResponse("Can't find patient by the card number")
        visit_type = request.POST['visitType']
        visit_subtype = request.POST['visitTypeDetail']

        time_interval_to_visit = request.POST['timeInterval']
        try:
            time_period = request.POST['timePeriod']
        except:
            time_period = 0
        obligatory_or_not = obveznost
        number_of_visits = request.POST['visitCount']

        type_of_visit = Vrsta_obiska.objects.get(ime=visit_subtype)

        #   Okolise je treba porihtat, kr drgac ne morm dodat celotnega naloga


        date_of_visit = request.POST['visitDate']
        date_of_visit = fix_date(date_of_visit)


        #   Create work task form
        work_task_f = Delovni_nalog(st_obiskov=number_of_visits, vrsta_obiska=type_of_visit,
                                    zdravnik=current_doc, datum_prvega_obiska=date_of_visit, cas_obiskov_dolzina=time_interval_to_visit)
        work_task_f.save()

        print("work tast form saved")

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


def work_task_form_processing(request):

    if request.method == 'POST':
        form = WorkTaskForm(request.POST)
        if form.is_valid():
            #   First i find the doctor object
            current_user = request.user
            try:
                current_doc = Zdravnik.objects.get(uporabniski_profil=current_user)
            except:
                return HttpResponse("Can't find this doctor(user) in the database")

            #   Tu se vnese od sessiona id.sifra

            nurse_id = form.cleaned_data['nurse_id']

            try:
                current_nurse = Patronazna_sestra.objects.get(sifra_patronazne_sestre=nurse_id)
            except:
                return  HttpResponse("Can't find current nurse")
            ZS = current_doc.sifra_izvajalca_ZS

            try:
                leader_PS = Vodja_PS.objects.get(sifra_izvajalca_ZS=ZS)
            except:
                return HttpResponse("Can't find vodja PS for this ZS")

            patient_card_id = form.cleaned_data['card_number']

            try:
                patient = Pacient.objects.get(st_kartice=patient_card_id)
            except:
                return HttpResponse("Can't find patient by the card number")

            type_of_visit = form.cleaned_data['visit_type']
            subtype_of_visit = form.cleaned_data['first_name']

            date_of_first_visit = form.cleaned_data['first_name']
            number_of_visits = form.cleaned_data['visit_count']
            time_interval = form.cleaned_data['first_name']
            time_period = form.cleaned_data['first_name']

            #   Create work task form
            work_task_f = Delovni_nalog(st_obiskov=number_of_visits, vrsta_obiska=type_of_visit, izvajalec_zs=ZS, zdravnik=current_doc, vodja_PS=leader_PS)
            work_task_f.save()
            #   Link task form with all patients
            #   TUKAJ MORAM NARDIT LOGIKO ZA VEC PACIENTOV (OTROCNIC) PO TEM KO DEJVID NARDI DO KONCA FORM.
            patient_wtf = Pacient_DN(delovni_nalog=work_task_f, pacient=patient)
            patient_wtf.save()

        else:
            print("Form not valid bro", form.errors)
            return HttpResponse("Form not valid")
    else:
        form = WorkTaskForm()

    return render(request, 'work_task.html', {'work_task_form': form})
