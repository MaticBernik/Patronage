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
from patronazna_sluzba_app.forms import  *
from patronazna_sluzba_app.models import *
import csv
import django.contrib.auth
import logging
import os
from itertools import chain


def list_patient_visitations(request):

    uporabnik = request.user
    
    visitations = Obisk.objects.all()
    material = Material_DN.objects.all()
    zdravila = Zdravilo_DN.objects.all()
    pacienti = Pacient_DN.objects.all()
    zdravniki = Zdravnik.objects.all()
    vodje_ps = Vodja_PS.objects.all()
    delovni_nalogi = Delovni_nalog.objects.all()
    vsa_nadomescanja = Nadomescanje.objects.all()

    visitations_complete = []
    visitations_waiting = []
    
    current_patient = Pacient.objects.get(uporabniski_profil=uporabnik)
    print("UPORABNIK",uporabnik)
    print("UPORABNIK ID", uporabnik.id)
    print("PACIENT:", current_patient)
    pacientDN=Pacient_DN.objects.filter(pacient=current_patient)
    print("pacientDN", pacientDN)
    nalogi_vezani_na_pacienta=[x.delovni_nalog_id for x in pacientDN]
    delovni_nalogi = delovni_nalogi.filter(id__in=nalogi_vezani_na_pacienta)
    
    print("delovni_nalog", delovni_nalogi)
    obiski_delovni_nalog = Delovni_nalog.objects.filter(id__in=[x.delovni_nalog_id for x in visitations])
    obiski_delovni_nalog = Delovni_nalog.objects.filter(id__in=nalogi_vezani_na_pacienta)
    visitations = Obisk.objects.filter(delovni_nalog_id__in=obiski_delovni_nalog)

    #visitations = visitations.filter(id__in=[x.id for x in visitations_nurse])
    print("VISITATIONS", visitations)
    visitations_complete = visitations.filter(opravljen=True)
    visitations_waiting = visitations.filter(opravljen=False)

    vsa_nadomescanja = Nadomescanje.objects.all()
    vsa_porocila = Porocilo_o_obisku.objects.all()
    vsa_polja_meritev = Polje_meritev.objects.all()
    vsa_pacient_DN = Pacient_DN.objects.all()

    context = {'work_task_list':delovni_nalogi, 'visitations_list_complete':visitations_complete,  'visitations_list_waiting':visitations_waiting, 'nbar': 'v_pat_visits', 'medications':zdravila, 'material': material, 'pacient_list': pacienti, 'doctors': zdravniki, 'head_nurses': vodje_ps, 'substitutions': vsa_nadomescanja, 'all_visit_reports': vsa_porocila, 'all_measure_fields': vsa_polja_meritev, 'all_p_DN': vsa_pacient_DN}
    return render(request, 'patient_visitations_list.html', context)

