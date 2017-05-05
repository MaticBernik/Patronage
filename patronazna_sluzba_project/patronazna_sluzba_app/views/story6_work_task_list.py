# -*- coding: utf-8 -*-
# @login_required(login_url='/')
from datetime import datetime
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
from patronazna_sluzba_app.forms import AddNursingPatientForm, ChangePasswordForm, LoginForm, PatientRegistrationFrom, RegisterMedicalStaffForm, WorkTaskForm
from patronazna_sluzba_app.models import Izvajalec_ZS, Pacient, Patronazna_sestra, Sodelavec_ZD, User, Vodja_PS, Zdravnik, Obisk, Delovni_nalog
import csv
import django.contrib.auth
import logging
import os

def is_doctor(user):
    if Zdravnik.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def is_leader_ps(user):
    if Vodja_PS.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def list_work_task(request):
    uporabnik = request.user
    # obiski = Obisk.objects
    # if is_doctor(uporabnik):
        # delovni_nalogi = Delovni_nalog.objects.filter(zdravnik=uporabnik)
    # elif is_leader_ps(uporabnik):
        # delovni_nalogi = Delovni_nalog.objects.filter(vodja_PS=uporabnik)
    # else:
        # print("ERROR!!")
        # return

    obiski = Obisk.objects.all()
    delovni_nalogi = Delovni_nalog.objects.all() 
    context = {'work_task_list':delovni_nalogi, 'visits_list':obiski, 'nbar': 'v_wrk_tsk'}
    return render(request, 'work_task_list.html', context)

