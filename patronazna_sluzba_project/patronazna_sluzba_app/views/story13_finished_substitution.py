#-*- coding: utf-8 -*-
# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
from datetime import date,datetime,timedelta
from django.db.models import Q
from math import floor
########################################################################


def finishedSubstitutionView(request):
    if request.method == "POST":
        form = SubstitutionFinishedForm(request.POST)
        nurse_chosen = request.POST['nurses']
        nurse = Patronazna_sestra.objects.get(id=int(nurse_chosen))
        print("================ "+nurse_chosen+" ==============")
        print("Izbrana sestra: " + str(nurse))
        print("==============================")
        q = Nadomescanje.objects.filter(sestra_id=int(nurse_chosen)).update(veljavno=False)
        print(q)
        #for i in q:
         #   print(i.veljavno)
        print("========UPDATED=======")
    else:

        form = SubstitutionFinishedForm()
    return render(request, 'nurse_sub_finished.html', {'substitution_form': form})