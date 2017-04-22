#from . import story2_create_pacient
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
#OLD: SPREMEMBA GESLA
# def change_password(pass1, pass2, id):
#   if story2_create_pacient.check_passwords(pass1, pass2):
#        user = User.objects.get(username=id)
#        user.set_password(pass1)
#        user.save()
#        return 1
#   return 0

#@login_required(login_url='/')
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():

            currentUser = request.user
           # print("Uporabnik: ")
            oldpassword =  form.cleaned_data['oldpassword']
            #print(currentUser.check_password(oldpassword))
            if currentUser.check_password(oldpassword):
                password1 = form.cleaned_data['password1'];
                password2 = form.cleaned_data['password2'];
                if password1 == password2 and len(password1)>7:
                    request.user.set_password(password1)
                    update_session_auth_hash(request, request.user)
                    request.user.save()
                    return render(request, 'base.html', context)
                    #user = User.objects.get(username=currentUser)
                    #user.set_password(password1)
                    #user.save()
                else:
                    return HttpResponse("Napaka pri potrditvi novega gesla!")
            else:
                return HttpResponse("Napačen vnos trenutnega gesla!")

    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'change_password_form': form})