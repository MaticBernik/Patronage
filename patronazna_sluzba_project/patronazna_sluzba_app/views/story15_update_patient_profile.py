# -*- coding: utf-8 -*-
# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
from datetime import date,datetime,timedelta
from django.db.models import Q
from math import floor


#   Funkcija, ki posodobi profil pacienta
def update_patient(user, st_kartice, telefonska, naslov, spol, datum_rojstva, ime, priimek, email, okolis, skrbnistvo, kontakt, posta, sorodstvo):
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
    if kontakt == '':
        kontakt = patient_profile.kontakt
    if posta == '':
        posta = patient_profile.posta
    if sorodstvo == '':
        sorodstvo = patient_profile.sorodstvo

    prof = patient_profile(st_kartice=st_kartice, telefonska_st=telefonska, naslov=naslov, spol=spol, datum_rojstva=datum_rojstva, ime=ime,
                           priimek=priimek, email=email, kontakt=kontakt, posta=posta, okolis=okolis, skrbnistvo=skrbnistvo, sorodstvo=sorodstvo)
    return prof
