# -*- coding: utf-8 -*-
# Create your views here.
# import the logging library
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.validators import validate_email
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.urls import reverse
from patronazna_sluzba_app.forms import *
from patronazna_sluzba_app.models import *
from . import story2_create_patient
import logging


# @user_passes_test(isAdmin,login_url='/')
def register_medical_staff(request):
    print("medical add")
    if request.method == 'GET':
        global context
        context={'medical_reg_form': RegisterMedicalStaffForm()}

        return render(request, 'medical_registration.html', context)
        # form = RegisterMedicalStaffForm()
        # return HttpResponse("THIS SHOULD BE IT.")
        # return render(request, 'medical_registration.html', {'medical_reg_form': form})
        # return render_to_response(request, 'medical_registration.html')
    else:
        #EXTRACT DATA FROM REQUEST
        #Extract standard user data from request

        form = RegisterMedicalStaffForm(request.POST)
        if form.is_valid():
            first_name =  form.cleaned_data['first_name']
            last_name =  form.cleaned_data['last_name']
            email =  form.cleaned_data['email']
            password1 = form.cleaned_data['password1']

            password2 =  form.cleaned_data['password2']
            # Extract additional staff specific data from request
            role =  form.cleaned_data['medic_role']
            print("ROLE = ", role)
            code =  form.cleaned_data['medical_id']
            phone_number = form.cleaned_data['phone_number']
            institution =  form.cleaned_data["medical_area_id"]

            institution = Izvajalec_ZS.objects.filter(st_izvajalca=institution)
            # work_location_number=request.POST['work_location_number']
            if len(institution) == 0:
                institution = None
            else:
                institution = institution[0]

            # VALIDATE FIELD VALUES
            # Validate passwords
            # or not password_validation.validate_password(password1)
            if not password1 == password2 or not len(password1) > 7:
                print("Invalid password.")
            # Validate email
            if not story2_create_patient.check_mail(email):
                print("Invalid email.")
            # Check if username(email) already exists
            if User.objects.filter(username=email).exists():
                print("Username is already taken.")
            # Check if nurse whith specified number already exists:
            if role == 'nurse' and Patronazna_sestra.objects.filter(sifra_patronazne_sestre=code).exists():
                print("Account with specified nurse number already exists.")
            elif role == 'doc' and Zdravnik.objects.filter(sifra_zdravnika=code):
                print("Account with specified doctor number already exists.")
            elif role == 'head_of_medical_service' and Vodja_PS.objects.filter(sifra_vodje_PS=code):
                print("Account with specified head of medical service number already exists.")
            elif role == 'employee' and Sodelavec_ZD.objects.filter(sifra_sodelavca=code):
                print("Account with specified employee number already exists.")
            # Validate phone number
            # Validate nurse number

            # CREATE AND SAVE NEW OBJECT TO DB
            # Create User object

            try:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password1,
                                                email=email,
                                                username=email)
                print("user object saved")
            except:
                print("Could not create User object using given data!")
                return HttpResponse("Userja ne gre registrirat.")
            # Finally create Nurse object

            if role == 'nurse':
                profile = Patronazna_sestra(uporabniski_profil=user, sifra_patronazne_sestre=code,
                                            telefonska_st=phone_number, sifra_izvajalca_ZS=institution,okolis_id=-1)
                print("delam sestro")
            elif role == 'doc':
                profile = Zdravnik(uporabniski_profil=user, sifra_zdravnika=code, telefonska_st=phone_number,
                                   sifra_izvajalca_ZS=institution)
                print("delam zdravnika")
            elif role == 'head_of_medical_service':
                profile = Vodja_PS(uporabniski_profil=user, sifra_vodje_PS=code, telefonska_st=phone_number,
                                   sifra_izvajalca_ZS=institution)
                print("delam vodjo PS")
            elif role == 'employee':
                profile = Sodelavec_ZD(uporabniski_profil=user, ssifra_sodelavca=code, telefonska_st=phone_number,
                                       sifra_izvajalca_ZS=institution)
                print("delam sodelavec_ZD")

            print("profil:", profile.uporabniski_profil.username)
            profile.save()
            """
            try:
                profile.save()
            except:
                print("Could not create "+role+" profile using given data!")
            """

        return redirect('link_control_panel')

