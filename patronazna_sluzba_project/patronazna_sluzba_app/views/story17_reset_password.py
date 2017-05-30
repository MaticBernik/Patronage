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


#@login_required(login_url='/')
def resetPasswordView(request):
    if request.method == "POST":
        reset_password_form = ForgottenPasswordForm(request.POST)

        if reset_password_form.is_valid():
            mail = request.POST['email']
            new_password  = request.POST['new_password1']
            act_token = mail+'|'+new_password
            # poslji mail za spremembo gesla. geslo se spremeni ob kliku na link.
            act_key = token.generate_token(act_token)

            sendEmail(act_key.decode("utf-8"), mail)
            print("mail je poslan")
            return HttpResponse("Na Vaš naslov smo poslali reset link")
        else:
            return HttpResponse("FORM IS INVALID "+str(reset_password_form.errors))
    else:
        reset_password_form = ForgottenPasswordForm()
        #context={'nbar': 'chng_pass', 'change_password_form': change_password_form}
        return render(request, 'forgotten_password.html', {'change_password_form':reset_password_form})


def change_pw_view(request):
    print("HAHAHAHA")
    if request.method == 'GET':
        act_key = request.GET.get('token', '')
        if act_key != '':

            print("Token value is: ")
            value = token.is_valid_token(act_key)
            print(value)
            mail_pw = value.split('|')
            print("mail ", mail_pw[0], "password ", mail_pw[1])
            try:
                user = User.objects.get(email=mail_pw[0])
                user.set_password(mail_pw[1])
                user.save()
                print("Geslo je spremenjeno")
                return HttpResponse("Geslo je spremenjeno. Poizkusite se vpisati.")
            except:
                print("Tega maila ni v nasi bazi")

    return HttpResponse("Sprememba gesla ni uspela.")


def sendEmail(activation_key, customer_mail):

    link="http://127.0.0.1:8000/activateNewPassword?token="+activation_key
    sporocilo = "Ob kliku na povezavo se vam bo geslo uspešno spremenilo.  "+link+" Želimo Vam lep dan, Parsek."

    send_mail(
        'Sprememba gesla. PARSEK',
        sporocilo,
        'change_password@parsekrules.si',
        [customer_mail],
        fail_silently=False,
    )
    print("mail poslan")
