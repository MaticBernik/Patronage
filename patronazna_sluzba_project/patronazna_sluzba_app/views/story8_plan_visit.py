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
#######TEST THE FUNCTIONALITY
global_plan=[]
global_nurse_id = 0
old_plan = []
def work_task_plan(request):
    if request.method == 'POST':

        try:
            visit_list = request.POST['visit_list']

            visit_list = visit_list.split()[0]
            print("THIS IS WHAT I GET: " + visit_list)
        except:
            print("EXCEPTION TRIGGERED no id_visit_list")

        #    visit_list = request.POST['id_plan_list']
        #    visit_list = visit_list.split()[0]
    else:
        visit_list ='7'

    task_fk = Pacient_DN.objects.select_related().filter(delovni_nalog_id=visit_list) #Delovni_nalog.objects.select_related().get(id=visit_list) #filter(id__iexact=visit_list)    #Okolis.objects.filter(id__iexact=visit_list)

    cas_obiskov_tip = task_fk[0].delovni_nalog.cas_obiskov_tip

    if cas_obiskov_tip == 'Interval':
        interval = int(task_fk[0].delovni_nalog.cas_obiskov_dolzina)
        visit_count = int(task_fk[0].delovni_nalog.st_obiskov)
        period =  interval * visit_count
    else:
        period = int(task_fk[0].delovni_nalog.cas_obiskov_dolzina)
        visit_count = int(task_fk[0].delovni_nalog.st_obiskov)
        interval = floor(period / visit_count)

    obisk = Obisk.objects.select_related().filter(delovni_nalog_id=visit_list)
    material = Material_DN.objects.select_related().filter(delovni_nalog_id=visit_list)#get(delovni_nalog_id=visit_list)
    medicine = Zdravilo_DN.objects.select_related().filter(delovni_nalog_id=visit_list)
    print('QUERY RESULT: '+str(task_fk)+'    '+str(material)+'  '+str(medicine))
   # task = Posta.objects.all()[1:10]
    return render_to_response('ajax_task_plan.html',{'task':task_fk,'material':material,'medicine':medicine,'obisk':obisk,'interval':interval,'period':period})

def is_nurse(user):
    if Patronazna_sestra.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def plan_list_ajax(request):

    if request.method == 'POST':
        #print("INSIDE POST BEFORE DATUM: ")
        datum = request.POST['datum']
        datum_format = datum.split('.')
        print("INSIDE POST: " + str(datum_format))
        datum = datum_format[2]+'-'+datum_format[1]+'-'+datum_format[0]
        print("INSIDE POST: " + datum)
    else:
        datum = ''
       #sestra za okoliš 18 vsi pacienti razen tone
    if is_nurse(request.user):
        nurse_profile_id = User.objects.get(username=request.user)

        # OBISKI KI SO V PLANU
        plan_list = Plan.objects.values_list('planirani_obisk_id',flat=True)
        global old_plan
        old_plan = plan_list

        """
         for field in Plan._meta.fields:
            print(field.name)

        test_ids = Subject.objects.all()
        result = Test.objects.filter(test_id__in=test_ids).filter([some other filtering])
        """

        #SE NEOPRAVLJENI OBISKI
        print("Sestra profil "+str(is_nurse(request.user))+' nurse profile id: '+str(nurse_profile_id.id))
        nurse=Patronazna_sestra.objects.get(uporabniski_profil_id =nurse_profile_id)

        #HARDCODE ABSENT NURSE ID
        try:
            absent = Nadomescanje.objects.get(nadomestna_sestra_id=nurse.id)
            fill_in = True
        except:
            fill_in = False

        #fill_in = True
        print('Medicinska sestra '+str(nurse.id))
        if len(plan_list) > 0:
            print("PLAN LIST ID "+str(plan_list[0]))

            print("plan ni prazen")
            #get the plan for the logged in sister
            if not fill_in:
                print("BREZ NADOMESCANJA")
                planned_visits = Obisk.objects.filter(id__in=plan_list).filter(p_sestra_id=nurse.id)#.filter(id__in=plan_list).order_by('datum')#filter(datum__gt=date.today())# #Okolis.objects.values_list('id','ime')
               # planned_visits=Plan.objects.select_related().filter(planirani_obisk.id__in=plan_list).filter(planirani_obisk.p_sestra_id=nurse_id)
                visit_list = Obisk.objects.filter(p_sestra_id=nurse.id).filter(~Q(id__in=plan_list))
            else:
                #vključi obiske sestre, ki jo nadomesca
                print("NADOMESCANJE")
                planned_visits = Obisk.objects.filter(id__in=plan_list).filter(Q(p_sestra_id=nurse.id)|Q(p_sestra_id=absent.sestra_id))
                visit_list = Obisk.objects.filter(Q(p_sestra_id=nurse.id)|Q(p_sestra_id=absent.sestra_id)).filter(~Q(id__in=plan_list))


            print("Query result")
            #add to global plan
            global global_plan



            for i in planned_visits:
                print('planirani: '+str(i.id))
            # get the planned visit from all visits
            test_plan = Plan.objects.select_related().filter(planirani_obisk_id__in=planned_visits).filter(datum__icontains=datum)
            test_plan = replace_datum_type(test_plan,1)
            #global_plan=planned_visits
            global_plan = test_plan

            print("GLOBAL PLAN")
            for i in global_plan:
                print(str(i.planirani_obisk))


            for i in planned_visits:
                print(i.p_sestra_id)
                #print(i.planirani_obisk_id)
        else:
            global global_plan
            global_plan = []
            if not fill_in:
                print("BREZ NADOMESCANJA PLAN JE PRAZEN")
                visit_list = Obisk.objects.select_related().filter(p_sestra_id=nurse.id).order_by('datum')
            else:
                # vključi obiske sestre, ki jo nadomesca
                print("NADOMESCANJE, PLAN JE PRAZEN")
                print("ABSENT NURSE: "+str(absent.sestra_id))
                visit_list = Obisk.objects.select_related().filter(Q(p_sestra_id=nurse.id) | Q(p_sestra_id=absent.sestra_id)).order_by('datum')



        print("Visit list "+str(len(visit_list)))
        visit_list = replace_datum_type(visit_list,0)

        #print('Datum tip: '+str(visit_list[0].obvezen_obisk))
        #print("todays date is: " + str(date.today()))
        #print("Tomorrow date is: " + str(date.today() + timedelta(days=1)))

        #OBISKI KI SO V PLANU
       # plan_list = Plan.objects.select_related().filter(p_sestra_id=nurse.id).order_by('datum')
        """
        id plan_obisk_id datum
        1   uniq
        2   uniq
        3   uniq
        better_list =[x[1] for x in visit_list]
        better_list_id = [x[0] for x in visit_list]
        for i in range(len(better_list)):
            better_list[i] = str(better_list_id[i])+' | '+better_list[i]
        #    print(i)
        """
    else:
        visit_list = []

    main_nurse_id = nurse.id
    global global_nurse_id
    global_nurse_id = nurse.id

    return render_to_response('ajax_plan_visit.html',{'visit_list':visit_list,'nurse':main_nurse_id})

def replace_datum_type(list,n):
    if n != 1:

        for i in list:
            if str(i.obvezen_obisk) == 'False':
                i.obvezen_obisk = 'Okviren'
            else:
                i.obvezen_obisk = 'Obvezen'
    else:
        for i in list:
            if str(i.planirani_obisk.obvezen_obisk) == 'False':
                i.planirani_obisk.obvezen_obisk = 'Okviren'
            else:
                i.planirani_obisk.obvezen_obisk = 'Obvezen'
    return list


def ajax_added_to_plan(request):

    return render_to_response('ajax_already_planned.html',{'planned':global_plan,'nurse':global_nurse_id})

def plan_visit_view(request):
    if request.method == "POST":
        visit_form = plan_visit_form(request.POST)
        plan_visit_list = request.POST.getlist('plan_list')
        plan = None

        global old_plan
       # print("OLDPLAN BEFORE: " + str(old_plan))
        #contained = [x for x in plan_visit_list if x in old_plan]
        #print("CONTAINED: "+str(contained))
        #for i in old_plan:
         #   print("old plan: "+str(i))
        if len(plan_visit_list) >= len(old_plan):

            for i in plan_visit_list:
                obisk_id = i.split(' ', 1)[0]
                print('Plan: '+obisk_id)
                if int(obisk_id) not in old_plan:
                    print("Ta obisk ni v bazi")
                    plan = Plan(planirani_obisk_id=obisk_id)
                    plan.save()
        else:
            pk_plan = [i[0] for i in plan_visit_list]
            results = list(map(int, pk_plan))
            for i in old_plan:
                if i not in results:
                    print("Ta obisk ni v planu")
                    plan = Plan.objects.get(planirani_obisk_id=str(i)).delete()
                    #plan.save()
        #old_plan = plan_visit_list
    else:
       visit_form = plan_visit_form()
    """
    print("GET REQUEST from view "+str( global_plan))
    for i in global_plan:
        print('View data: '+str(i))
    """
    return render(request, 'plan_visit.html', {'plan_visit_form': visit_form})