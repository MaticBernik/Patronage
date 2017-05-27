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
        patient_profile = Pacient.objects.get(uporabniski_profil=patient_user)
        district = request.POST['search_district']
        card = patient_profile.st_kartice
        birth_date = patient_profile.datum_rojstva
        sex = patient_profile.spol
        mail = patient_profile.email
        rel = request.POST.get('contact_sorodstvo', False)

        print("RELATION",rel)
        update_patient(patient_user, card ,request.POST['phone_number'],
                                 request.POST['address'], sex, birth_date,
                                 request.POST['first_name'], request.POST['last_name'], mail,
                                 request.POST['search_district'], request.POST['search_post'], request.POST['contact_first_name'], request.POST['contact_last_name'], request.POST['contact_address'], request.POST['contact_phone_number'], rel)

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


def update_patient(user, st_kartice, telefonska, naslov, spol, datum_rojstva, ime, priimek, email, okolis, posta,
                   contact_last_name, contact_first_name, contact_address, contact_phone_number, contact_sorodstvo):
    patient_profile = Pacient.objects.get(uporabniski_profil=user)
    print("pacieeeeeent", patient_profile.ime)

    patient_profile.st_kartice = st_kartice
    patient_profile.telefonska_st = telefonska
    patient_profile.naslov = naslov
    patient_profile.datum_rojstva = datum_rojstva
    patient_profile.ime = ime
    patient_profile.priimek = priimek

    okolis = Okolis.objects.get(ime=okolis)
    patient_profile.okolis = okolis

    posta = Posta.objects.get(postna_st=int(posta[:4]))
    patient_profile.posta = posta

    contact = patient_profile.kontakt
    if contact is None:
        contact = Kontaktna_oseba()
        contact.save()
    if contact_first_name != '':
        contact.ime = contact_first_name
        contact.save()
    if contact_last_name != '':
        contact.priimek = contact_last_name
        contact.save()
    if contact_address != '':
        contact.naslov = contact_address
        contact.save()
    if contact_phone_number != '':
        contact.telefon = contact_phone_number
        contact.save()
    if contact_phone_number != '':
        contact.telefon = contact_phone_number
        contact.save()
    if contact_sorodstvo is not False:
        rel = Sorodstveno_razmerje(kontakt=contact, pacient_id=patient_profile, tip_razmerja=contact_sorodstvo)
        rel.save()
        contact.sorodstvo = rel
        contact.save()
        print("sorodstvo", rel.tip_razmerja)

    print("contact", contact.ime)


    patient_profile.kontakt = contact
    patient_profile.save()
    return 1
