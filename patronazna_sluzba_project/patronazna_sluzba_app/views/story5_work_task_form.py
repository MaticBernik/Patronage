# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect


def work_task_form_processing(request):

    if request.method == 'POST':
        form = WorkTaskForm(request.POST)
        if form.is_valid():
            #   Tu se vnese od sessiona id.sifra
            doctor_id = 0
            nurse_id = 0 #  Stevilka izvajalca
            work_task_form_id = 0
            type_of_visit = 0
            subtype_of_visit = 0
            patient_card_id = 0
            date_of_first_visit = 0
            number_of_visits = 0
            time_interval = 0
            time_period = 0

            #   Ustvari delovni nalog

            #   Polinkaj delovni nalog z vsemi pacienti (otrocnica otrok..)

            #   Shrani delovni nalog


        else:
            print("Form not valid bro", form.errors)
            return HttpResponse("Form not valid")
    else:
        form = WorkTaskForm()

    return render(request, 'work_task.html', {'work_task_form': form})
