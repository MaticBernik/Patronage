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
def update_patient(user, st_kartice, telefonska, naslov, spol, datum_rojstva, ime, priimek, email, okolis_id, skrbnistvo_id):

    return 1