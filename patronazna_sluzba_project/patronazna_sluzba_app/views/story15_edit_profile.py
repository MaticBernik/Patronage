# -*- coding: utf-8 -*-
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from patronazna_sluzba_app import token
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from patronazna_sluzba_app.forms import *

def editProfileView(request):

    #form = FormEditCoworker(instance=instance)
    if request.method == 'POST':
        print("POST")
    else:
        print("GET")
    #form = PatientRegistrationFrom()

    form = EditProfileForm(user=request.user)#user=request.user)
    print("========LOGIRANI PACIENT=========")
    patient_q = Pacient.objects.select_related().get(uporabniski_profil=request.user)
    print(patient_q)
    return render(request, 'update_profile.html', {'registration_form': form,'patient':patient_q})

def editNursingProfileView(request,id="0"):
    # form = FormEditCoworker(instance=instance)
    if request.method == 'POST':
        print("POST lalalla")
        nursing_card = request.POST['card_number']
        print("#########STEVILKA OSKRBOVANCA ########")
        print(nursing_card)
    else:
        print("GET gegege")
    # form = PatientRegistrationFrom()

    form = EditNursingProfileForm(user=id)  # user=request.user)
    print("========ST OSKRBOVANCA=========")
    print(id)
    patient_q = Pacient.objects.select_related().get(st_kartice=id)
    print(patient_q)
    return render(request, 'edit_nursing_profile.html', {'add_nursing_patient_form': form, 'patient': patient_q})