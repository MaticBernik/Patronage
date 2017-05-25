# -*- coding: utf-8 -*-
#from . import story2_create_pacient
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.contrib.auth import update_session_auth_hash

#@login_required(login_url='/')
def resetPasswordView(request):
    if request.method == "POST":
        reset_password_form = ForgottenPasswordForm(request.POST)

        if reset_password_form.is_valid():
            return HttpResponse("Na Vašem naslovu smo poslali reset link")
        else:
            return HttpResponse("FORM IS INVALID "+str(reset_password_form.errors))
        """
            currentUser = request.user
           # print("Uporabnik: ")
            old_password =  form.cleaned_data['old_password']
            #print(currentUser.check_password(oldpassword))
            if currentUser.check_password(old_password):
                password1 = form.cleaned_data['new_password1'];
                password2 = form.cleaned_data['new_password2'];
                if password1 == password2 and len(password1)>7:
                    request.user.set_password(password1)
                    update_session_auth_hash(request, request.user)
                    request.user.save()
                    return render(request, 'base_panel.html')
                    #user = User.objects.get(username=currentUser)
                    #user.set_password(password1)
                    #user.save()
                else:
                    return HttpResponse("Napaka pri potrditvi novega gesla!")
            else:
                return HttpResponse("Napačen vnos trenutnega gesla!")
        """
        #return redirect('link_logout')
    else:
        reset_password_form = ForgottenPasswordForm()
        #context={'nbar': 'chng_pass', 'change_password_form': change_password_form}
        return render(request, 'forgotten_password.html', {'change_password_form':reset_password_form})