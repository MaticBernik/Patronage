# -*- coding: utf-8 -*-
#from . import story2_create_pacient
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.contrib.auth import update_session_auth_hash
from patronazna_sluzba_app import token
from patronazna_sluzba_app.models import User
from django.core.mail import send_mail

 
def disable_patient_user(request):
    user = request.user
    
    if(request.POST):
        form = DeleteUserForm(request.POST)
        conf_pass = request.POST['confirm_pass']

        if(user.password == conf_pass):
            print("same pass")
            user.is_active = False
            return HttpResponseRedirect('link_home')
        

    form = DeleteUserForm()
    context = {'nbar': 'u_del', 'delete_patient_form': form}
    return render(request, 'delete_user.html', context)
    

    
def disable_staff_member():
    pass