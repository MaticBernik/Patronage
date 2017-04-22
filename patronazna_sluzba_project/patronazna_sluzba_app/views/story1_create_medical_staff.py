# Create your views here.
# import the logging library
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.validators import validate_email
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render
from django.template import Context, loader
from django.template import RequestContext
from django.urls import reverse
from patronazna_sluzba_app.forms import LoginForm
from patronazna_sluzba_app.models import Pacient,Patronazna_sestra,Sodelavec_ZD,User,Vodja_PS,Zdravnik
import logging

def register_medical_staff(request):
    if request.method == 'POST':
        #EXTRACT DATA FROM REQUEST
        #Extract standard user data from request
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        #Extract additional staff specific data from request
        role=request.POST['role']
        code=request.POST['medical_id']
        phone_number=request.POST['phone_number']
        institution=request.POST["medical_area_id"]
        #work_location_number=request.POST['work_location_number']

        #VALIDATE FIELD VALUES
        #Validate passwords
        if not password1==password2 and password_validation.validate_password(password1):
            print("Invalid password.")
        #Validate email
        if not validate_email(email):
            print("Invalid email.")
        #Check if username(email) already exists
        if User.objects.filter(username=email).exists():
            print("Username is already taken.")
        #Check if nurse whith specified number already exists:
        if role=='nurse' and Patronazna_sestra.objects.filter(sifra_patronazne_sestre=code).exists():
            print("Account with specified nurse number already exists.")
        elif role=='doc' and Zdravnik.objects.filter(sifra_zdravnika=code):
            print("Account with specified doctor number already exists.")
        elif role=='head_of_medical_service' and Vodja_PS.objects.filter(sifra_vodje_PS=code):
            print("Account with specified head of medical service number already exists.")
        elif role=='employee' and Sodelavec_ZD.objects.filter(sifra_sodelavca=code):
            print("Account with specified employee number already exists.")
        #Validate phone number
        #Validate nurse number

        #CREATE AND SAVE NEW OBJECT TO DB
        #Create User object
        user=User(first_name=first_name,last_name=last_name,password=password1,email=email,username=email)
        try:
            user.save()
        except:
            print("Could not create User object using given data!")
        #Finally create Nurse object
        nurse = Patronazna_sestra(uporabniski_profil=user,sifra_patronazne_sestre=code,telefonska_st=phone_number)
        try:
            nurse.save()
        except:
            print("Could not create Nurse object using given data!")


def index(request):
    user = request.user
    if request.method=='GET':
        template=loader.get_template('index.html')
        context = {
            'login_form': LoginForm()
        }
        return HttpResponse(template.render(context))
    elif request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password )
            print('Login: ',username)
            if user is not None:
                login(request, user)
                if Patronazna_sestra.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_nurse/')
                elif Vodja_PS.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_ps_leader/')
                elif Zdravnik.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_doctor/')
                elif Sodelavec_ZD.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_employee/')
                elif Pacient.objects.filter(uporabniski_profil=user).exists():
                    return HttpResponseRedirect('home_patient/')
            else:
                print("Unsuccessful user authentication.")
                return HttpResponseRedirect('/')
        else:
            print("Invalid form!")
            return HttpResponseRedirect('/')

