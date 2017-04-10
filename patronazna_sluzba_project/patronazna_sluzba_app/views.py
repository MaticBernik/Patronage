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
from .models import User,Vodja_PS,Zdravnik,Patronazna_sestra,Sodelavec_ZD,Pacient


# Create your views here.
def index(request):
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

