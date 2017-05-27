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
        patient_user = request.user
        profile = update_patient(patient_user, request.POST['card_number'],request.POST['phone_number'],
                                 request.POST['address'], request.POST['sex'], request.POST['birth_date'],
                                 request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                                 okolis, skrbnistvo, kontakt, posta, sorodstvo)
        profile.save()
        print("POST")
    else:
        print("GET")
    #form = PatientRegistrationFrom()

    form = EditProfileForm(user=request.user)
    print("======== PACIENT=========")
    patient_q = Pacient.objects.select_related().get(uporabniski_profil=request.user)
    print(patient_q)
    print("==============SPOl===========")
    print(patient_q.spol)
    return render(request, 'update_profile.html', {'registration_form': form,'patient':patient_q})

def editNursingProfileView(request,id="0"):
    # form = FormEditCoworker(instance=instance)
    if request.method == 'POST':
        print("POST")

    else:
        print("GET")
    # form = PatientRegistrationFrom()

    form = EditNursingProfileForm(user=id)  # user=request.user)
    print("========ST OSKRBOVANCA=========")
    print(id)
    patient_q = Pacient.objects.select_related().get(st_kartice=id)
    print("============COMPARISON================")
    print("Skrbnistvo: "+str(patient_q.skrbnistvo.uporabniski_profil.username)+" DOSTOPA: "+str(request.user))
    print("============================")
    if str(patient_q.skrbnistvo.uporabniski_profil.username) != str(request.user):
        return HttpResponse("Nimate pravice dostopa do tega profila")
    else:
        print(patient_q)
        return render(request, 'edit_nursing_profile.html', {'add_nursing_patient_form': form, 'patient': patient_q})


def update_patient(user, st_kartice, telefonska, naslov, spol, datum_rojstva, ime, priimek, email, okolis, skrbnistvo, posta, sorodstvo,
                   contact_last_name, contact_first_name, contact_address, contact_phone_number, contact_sorodstvo):
    patient_profile = Pacient.objects.get(uporabniski_profil=user)
    if st_kartice == '':
        st_kartice = patient_profile.st_kartice
    if telefonska == '':
        telefonska = patient_profile.telefonska
    if naslov == '':
        naslov = patient_profile.naslov
    if spol == '':
        spol = patient_profile.spol
    if datum_rojstva == '':
        datum_rojstva = patient_profile.datum_rojstva
    if ime == '':
        ime = patient_profile.ime
    if priimek == '':
        priimek = patient_profile.priimek
    if email == '':
        email = patient_profile.email
    if okolis == '':
        okolis = patient_profile.okolis
    if skrbnistvo == '':
        skrbnistvo = patient_profile.skrbnistvo
#   DODAJ KONTAKT
    if posta == '':
        posta = patient_profile.posta
    if sorodstvo == '':
        sorodstvo = patient_profile.sorodstvo

    prof = patient_profile(st_kartice=st_kartice, telefonska_st=telefonska, naslov=naslov, spol=spol, datum_rojstva=datum_rojstva, ime=ime,
                           priimek=priimek, email=email, kontakt=kontakt, posta=posta, okolis=okolis, skrbnistvo=skrbnistvo, sorodstvo=sorodstvo)
    return prof
