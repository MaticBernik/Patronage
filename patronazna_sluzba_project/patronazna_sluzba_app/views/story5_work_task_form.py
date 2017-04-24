# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect


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
