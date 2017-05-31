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
########################################################################



def substitutionView(request):
    if request.method == "POST":
        date_start = request.POST['start_date']
        date_end = request.POST['end_date']
        print("DATE", date_end)

        nurse = request.POST['search_nurse']
        nurse = Patronazna_sestra.objects.get(sifra_patronazne_sestre=nurse[0:5])

        sub_nurse = request.POST['nurse_sub']
        sub_nurse = Patronazna_sestra.objects.get(sifra_patronazne_sestre=sub_nurse[0:5])

        date_start = datetime.strptime(date_start, "%d.%m.%Y")
        date_end = datetime.strptime(date_end, "%d.%m.%Y")

        substitution = Nadomescanje(sestra=nurse, datum_zacetek=date_start, datum_konec=date_end,
                                    nadomestna_sestra=sub_nurse)
        substitution.save()

        sub_array = Nadomescanje.objects.filter(nadomestna_sestra=nurse)
        for i in sub_array:
            sub = Nadomescanje()
            #   | Z K |
            if i.datum_zacetek <= date_start and i.datum_konec >= date_end:
                sub = Nadomescanje(sestra=i.sestra, datum_zacetek=date_start, datum_konec=date_end, nadomestna_sestra=sub_nurse, veljavno=1)

                print("| Z K |")
            #   | Z | K
            if i.datum_zacetek <= date_start and i.datum_konec > date_start and i.datum_konec <= date_end:
                sub = Nadomescanje(sestra=i.sestra, datum_zacetek=date_start, datum_konec=i.datum_konec, nadomestna_sestra=sub_nurse, veljavno=1)

                print(" | Z | K")
            #   Z | K |
            if i.datum_zacetek >= date_start and i.datum_zacetek < date_end and i.datum_konec >= date_end:
                sub = Nadomescanje(sestra=i.sestra, datum_zacetek=i.datum_zacetek, datum_konec=date_end, nadomestna_sestra=sub_nurse, veljavno=1)

                print("Z | K |")
            #   Z | | K
            if i.datum_zacetek >= date_start and i.datum_zacetek < date_end and i.datum_konec > date_start and i.datum_konec < date_end:
                sub = Nadomescanje(sestra=i.sestra, datum_zacetek=i.datum_zacetek, datum_konec=i.datum_konec, nadomestna_sestra=sub_nurse, veljavno=1)

                print("Z | | K")
            sub.save()
        return HttpResponse("Nadomescanje dodano.")

    else:
        print("GET REQUEST")
    substitution_form = SubstituteSisterForm()
    """
    print("GET REQUEST from view "+str( global_plan))
    for i in global_plan:
        print('View data: '+str(i))
    """
    return render(request, 'nurse_substitution.html', {'substitution_form': substitution_form})

def ajax_nurse_autocomplete(request):
    if request.method == 'POST':
        nurse = request.POST['search_nurse']
    else:
        nurse =''
    #seznam idjev vseh odsotnih sester
    absent_nurses = Nadomescanje.objects.values_list('sestra_id', flat=True) #get(nadomestna_sestra_id=nurse.id) Plan.objects.values_list('planirani_obisk_id', flat=True)
    print("========================ABSENT NURSES=========")
    print(absent_nurses)
    nurses = Patronazna_sestra.objects.filter(~Q(id__in=absent_nurses)).filter(uporabniski_profil__first_name__icontains=nurse) #filter(~Q(id__in=plan_list))

    return render_to_response('ajax_nurses.html', {'nurses': nurses})

def ajax_sub_nurse(request):
    if request.method == 'POST':
        nurse = request.POST['search_nurse']
        nurse_sifra = nurse.split(' ',1)[0]
        nurse = Patronazna_sestra.objects.get(sifra_patronazne_sestre=nurse_sifra)
        nurse_id = nurse.id
        print("========QUERY NURSE=======")
        print(nurse_id)
        sub_nurse = request.POST['nurse_sub']
    else:
        nurse_id = -1
        sub_nurse = ''
    #seznam idjev vseh odsotnih sester
    absent_nurses = Nadomescanje.objects.values_list('sestra_id', flat=True) #get(nadomestna_sestra_id=nurse.id) Plan.objects.values_list('planirani_obisk_id', flat=True)
    print("========================ABSENT NURSES 2=========")
    print(absent_nurses)
    print("nurse_id "+str(nurse_id))
    print("SUBNURSE: "+sub_nurse)
    nurses = Patronazna_sestra.objects.filter(~Q(id__in=absent_nurses)).filter(~Q(id=int(nurse_id))).filter(uporabniski_profil__first_name__icontains=sub_nurse) #filter(~Q(id__in=plan_list))

    return render_to_response('ajax_sub_nurses.html', {'nurses': nurses})
