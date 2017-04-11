#from django.contrib.auth import password_validation
import django.contrib.auth
from django.core.validators import validate_email
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
#from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import LoginForm
from .forms import RegistrationFrom
from .models import User,Vodja_PS,Zdravnik,Patronazna_sestra,Sodelavec_ZD,Pacient
import kreiranje_pacienta_zgodba2
#def index(request):
#
#	# if this is a POST request we need to process the form data
#    if request.method == 'POST':
#            #return HttpResponseRedirect('/thanks/')
#            return HttpResponse("Thanks, for trying.")
#    # if a GET (or any other method) we'll create a blank form
#    else:
#        form = LoginForm()
#
#    return render(request, 'index.html', {'login_form': form})



# Create your views here.
def index(request):
    if request.method=='GET':
        form = LoginForm()
        return render(request, 'index.html', {'login_form': form})
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
        return HttpResponse("Thanks for trying.")

def register(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
            #return HttpResponseRedirect('/thanks/')

            password1 = request.POST['']
            password2 = request.POST['']
            name = request.POST['']
            surname = request.POST['']
            mail = request.POST['']
            card_number = request.POST['']
            address = request.POST['']
            county_number = request.POST['']
            phone_number = request.POST['']
            birth_date = request.POST['']
            sex = request.POST['']
            contact_name = request.POST['']
            contact_surname = request.POST['']
            contact_address = request.POST['']
            contact_phone_number = request.POST['']
            sorodstveno_razmerje = request.POST['']

            if not (kreiranje_pacienta_zgodba2.add_patient_caretaker(password1, password2, name, surname, mail,
                                                                    card_number, address, county_number, phone_number,
                                                                    birth_date, sex, contact_name,
                                                                    contact_surname, contact_address,
                                                                    contact_phone_number, sorodstveno_razmerje)):
                return HttpResponse("Nekdo posile requeste napisane na roko... al pa mi se funkcije ne delajo")

            return HttpResponse("Thanks for registering")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationFrom()

    return render(request, 'register.html', {'registration_form': form})


def changePassword(request):

    return render(request, 'changePassword.html')
