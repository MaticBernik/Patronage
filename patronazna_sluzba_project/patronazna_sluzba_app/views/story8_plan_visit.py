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
from django.contrib import messages
########################################################################
#######TEST THE FUNCTIONALITY
#global_plan=[]
#global_nurse_id = 0
#old_plan = []
#main_nurse = None


def material_list(request):
    print("=============GLOBAL PLAN MATERIAL============")
    medicine = {}
    blood_tubes = {}
    """TRY SESSION"""
    global_plan = request.session.get('global_plan')
    for i in global_plan:
        tip_obiska = str(i.planirani_obisk.delovni_nalog.vrsta_obiska.ime)
        delovni_nalog_id = str(i.planirani_obisk.delovni_nalog_id)

        if tip_obiska == 'Odvzem krvi':
            # print("Epruvete")
            tube_query = Material_DN.objects.select_related().filter(delovni_nalog_id=delovni_nalog_id)
            for j in tube_query:
                tube_name = j.material.ime
                if tube_name in blood_tubes:
                    blood_tubes[tube_name] += j.kolicina
                else:
                    blood_tubes[tube_name] = j.kolicina


        elif tip_obiska == 'Aplikacija injekcij':
            # print("Zdravila: ")
            medicine_query = Zdravilo_DN.objects.select_related().filter(delovni_nalog_id=delovni_nalog_id)
            for j in medicine_query:
                m_name = j.zdravilo.kratko_poimenovanje
                if m_name in medicine:
                    medicine[m_name] += 1
                else:
                    medicine[m_name] = 1
    print("=========MATERIAL ZA OBISK=================")
    print("ZDRAVILA:")
    print(medicine)
    print("EPRUVETE")
    print(blood_tubes)

    return render_to_response('ajax_material_list.html',{'medicine':medicine,'blood_tubes':blood_tubes})


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
    #rel_obj = getattr(instance, self.cache_name) AttributeError: 'MyModel' object has no attribute '_zdravnik_cache'
    task_fk = Pacient_DN.objects.select_related().filter(delovni_nalog_id=visit_list) #Delovni_nalog.objects.select_related().get(id=visit_list) #filter(id__iexact=visit_list)    #Okolis.objects.filter(id__iexact=visit_list)

    delovni_nalog = Delovni_nalog.objects.select_related().filter(id=visit_list)

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
    print("####################################")
    for field in Delovni_nalog._meta.fields:
        print(field.name)
    print('QUERY RESULT: '+str(delovni_nalog[0].zdravnik)+'    '+str(material)+'  '+str(medicine))
    print("####################################")
   # task = Posta.objects.all()[1:10]
    #global main_nurse
    main_nurse = request.session.get('main_nurse')
    main_nurse = Patronazna_sestra.objects.get(id=main_nurse)
    return render_to_response('ajax_task_plan.html',{'task':task_fk,'material':material,'medicine':medicine,'obisk':obisk,'interval':interval,'period':period,'main_nurse':main_nurse})

def is_nurse(user):
    if Patronazna_sestra.objects.filter(uporabniski_profil=user).exists():
        return True
    return False

def plan_list_ajax(request):

    #global global_plan

    if request.method == 'POST':
        #print("INSIDE POST BEFORE DATUM: ")
        datum = request.POST['datum']
        if datum != '':
            datum_format = datum.split('.')
            print("INSIDE POST: " + str(datum_format))
            datum = datum_format[2]+'-'+datum_format[1]+'-'+datum_format[0]
            print("INSIDE POST: " + datum)
            #datum_plan = datum
        else:
            datum = datetime.now().date()
            #datum_plan = (datetime.now().date() + timedelta(days=1, hours=2))
    else:
        try:
            datum = request.GET['datum']
        except:
            datum=''
        if datum != '':
            datum_format = datum.split('.')
            print("INSIDE POST: " + str(datum_format))
            datum = datum_format[2] + '-' + datum_format[1] + '-' + datum_format[0]
            print("INSIDE POST: " + datum)
            # datum_plan = datum
        else:
            datum = datetime.now().date()
            # datum_plan = (datetime.now().date() + timedelta(days=1, hours=2))

        print("----------------GET DATUM-------------")
        print(datum)
       # datum = datetime.now().date()
       #datum_plan = (datetime.now().date() + timedelta(days=1, hours=2))
       #sestra za okoliš 18 vsi pacienti razen tone
    if is_nurse(request.user):
        nurse_profile_id = User.objects.get(username=request.user)

        # OBISKI KI SO V PLANU
        plan_list = Plan.objects.values_list('planirani_obisk_id',flat=True)
        #global old_plan
        #old_plan = Plan.objects.filter(datum__icontains=datum).values_list('planirani_obisk_id',flat=True) #(datetime.now().date() + timedelta(days=1))

        print("Sestra profil " + str(is_nurse(request.user)) + ' nurse profile id: ' + str(nurse_profile_id.id))
        nurse = Patronazna_sestra.objects.get(uporabniski_profil_id=nurse_profile_id)
        """
        print("=========================================")
        print("=========OLD PLAN NEW QUERY============")
        print("NURSE ID FOR OLD PLAN: "+str(nurse.id))
        print(old_plan)
        print((datetime.now().date() + timedelta(days=1)))
        print("=========================================")
        """


        """
         for field in Plan._meta.fields:
            print(field.name)

        test_ids = Subject.objects.all()
        result = Test.objects.filter(test_id__in=test_ids).filter([some other filtering])
        """

        #SE NEOPRAVLJENI OBISKI
        #print("Sestra profil "+str(is_nurse(request.user))+' nurse profile id: '+str(nurse_profile_id.id))
        #nurse=Patronazna_sestra.objects.get(uporabniski_profil_id =nurse_profile_id)
        #trenutna sestra rabimo pri izpisu nadomestne sestre
        #global main_nurse
        request.session['main_nurse'] = nurse.id

        """TRY SESSION"""
        """BUG obisk vezan na logged in nurse"""
        """PREVERI ALI JE SESTRA ODSOTNA IN ONEMOGOČI PLANIRANJE"""
        try:
            current_nurse_absent = Nadomescanje.objects.filter(sestra_id=nurse.id,veljavno=True,datum_zacetek__lte=date.today(),datum_konec__gte=date.today())
            print(current_nurse_absent)
        except:
            print("QUERY ERROR!!!!!!!!!!!!!!!!!!")
        print(date.today())

        old_plan = Plan.objects.filter(datum__icontains=datum, planirani_obisk__p_sestra_id=nurse.id,planirani_obisk__n_sestra_id=None).values_list('planirani_obisk_id', flat=True)
        old_plan |= Plan.objects.filter(datum__icontains=datum, planirani_obisk__n_sestra_id=nurse.id).values_list('planirani_obisk_id', flat=True)

        """
            #sestra je odsotna
            print("===========LOGIRANA SESTRA JE ODSOTNA=========")
            old_plan = Plan.objects.filter(datum__icontains=datum,planirani_obisk__p_sestra_id=nurse.id).values_list('planirani_obisk_id', flat=True)
        else:
            print("===============LOGIRANA SESTRA NI ODSOTNA========")
            old_plan = Plan.objects.filter(datum__icontains=datum,planirani_obisk__p_sestra_id=nurse.id).values_list('planirani_obisk_id', flat=True)
        # request.session.get('old_plan')
        """
        """if not old_plan:
            old_plan = Plan.objects.filter(datum__icontains=datum).filter(planirani_obisk__p_sestra_id=nurse.id).values_list('planirani_obisk_id', flat=True)
        """

        try:
            #absent = Nadomescanje.objects.get(nadomestna_sestra_id=nurse.id)
            #id vseh sester, ki jih je nadomeščala (1,5,10,11...)
            #absent = Nadomescanje.objects.filter(nadomestna_sestra_id=nurse.id).filter(veljavno=True)#.values_list('sestra_id',flat=True)
            absent = Nadomescanje.objects.filter(nadomestna_sestra_id=nurse.id,veljavno=True)#.values_list('sestra_id',flat=True)
            absent_ids = set()
            query= Nadomescanje.objects.filter(nadomestna_sestra_id=nurse.id,veljavno=True).values_list('sestra_id',flat=True)
            absent_ids.update(query)
            #preveri ali sestra, ki jo nadomecam že nadomešča drugo sestro
            """for x in absent:
                absent |= Nadomescanje,objects.filter(nadomestna_sestra_id=x.sestra_id).filter(veljavno=True)
            """
            print("==================ABSENTEE====================")
            if len(absent) > 0:
                fill_in = True
                print(absent_ids)
                """
                for x in absent_ids:
                    absent |= Nadomescanje.objects.filter(nadomestna_sestra_id=x).filter(veljavno=True)
                    query = Nadomescanje.objects.filter(nadomestna_sestra_id=x).filter(veljavno=True).values_list('sestra_id', flat=True)
                    absent_ids.update(query)
                """
                print(absent_ids)
                print("<<<<<<<<<<<<<NADOMESCANJE OBSTAJA QUERY IN ALL ABSENT NURSES>>>>>>>>>>>>>>")
                print(old_plan)
                #old_plan |= Plan.objects.filter(datum__icontains=datum,planirani_obisk__p_sestra_id__in=absent_ids).values_list('planirani_obisk_id', flat=True)

                """
                for i in absent:
                    print("Start: "+str(i.datum_zacetek)+" END: "+str(i.datum_konec))
                """
            else:
                print("PRAZNO ABSENTEE")
                fill_in = False
            print("================THIS PRINTS======================")

            #absent = Nadomescanje.objects.get(nadomestna_sestra_id=nurse.id)
        except:
            fill_in = False
        """JSON SERIALIZATION"""
        temp_list = []
        for value in old_plan:
            temp_list.append(value)
        old_plan = temp_list
        print("==============OLD PLAN ON GET METHOD=========")
        print(old_plan)
        request.session['old_plan'] = old_plan
        print('Medicinska sestra '+str(nurse.id))
        if len(plan_list) > 0:
            print("PLAN LIST ID "+str(plan_list[0]))

            print("plan ni prazen")
            #get the plan for the logged in sister
            if not fill_in:
                print("BREZ NADOMESCANJA")
                if len(current_nurse_absent)>0:
                    absent_visits = set()
                    for i in current_nurse_absent:
                        """GET ALL VISITS WHILE ABSENT AND FILTER BASED ON THOSE"""
                        query = Obisk.objects.filter(p_sestra_id=nurse.id,datum__range = (i.datum_zacetek, i.datum_konec)).values_list('id',flat=True)#.filter(~Q(id__in=plan_list)).values_list('id',flat=True)
                        absent_visits.update(query)
                        print(absent_visits)
                    visit_list = Obisk.objects.filter(~Q(id__in=plan_list),~Q(id__in=absent_visits),p_sestra_id=nurse.id).order_by('datum')
                    planned_visits = Obisk.objects.filter(Q(id__in=plan_list),~Q(id__in=absent_visits),p_sestra_id=nurse.id,n_sestra_id=None)
                    planned_visits |= Obisk.objects.filter(Q(id__in=plan_list), ~Q(id__in=absent_visits),n_sestra_id=nurse.id)
                    #planned_visits = []
                    print("PLANIRANI OBISKI  1111: ")
                    print(plan_list)
                    print(planned_visits)
                else:
                    #absent_all = Nadomescanje.objects.filter(sestra_id=nurse.id)
                    visit_list = Obisk.objects.filter(~Q(id__in=plan_list),p_sestra_id=nurse.id).order_by('datum')
                    planned_visits = Obisk.objects.filter(id__in=plan_list,p_sestra_id=nurse.id,n_sestra_id=None)#.filter(id__in=plan_list).order_by('datum')#filter(datum__gt=date.today())# #Okolis.objects.values_list('id','ime')
                    planned_visits |= Obisk.objects.filter(id__in=plan_list, n_sestra_id=nurse.id)
                   # planned_visits=Plan.objects.select_related().filter(planirani_obisk.id__in=plan_list).filter(planirani_obisk.p_sestra_id=nurse_id)
                    """
                    Iz plana vseh obiskov določene sestre izloči obiske, ki jih je opravila nadomesta sestra
                    """
                    """
                    for i in absent_all:
                        planned_visits |= Obisk.objects.filter(id__in=plan_list).filter(p_sestra_id=nurse.id).filter(~Q(datum__range = (i.datum_zacetek, i.datum_konec)))
                    print("PLANIRANI OBISKI 2222: ")
                    print(planned_visits)
                    """
            else:
                #vključi obiske sestre, ki jo nadomesca
                print("NADOMESCANJE")
                #planned_visits = Obisk.objects.filter(id__in=plan_list).filter(Q(p_sestra_id=nurse.id)|Q(p_sestra_id=absent.sestra_id),Q(datum__gte=datetime.date(2017, 6, 1)))
                #planned_visits = Obisk.objects.filter(id__in=plan_list).filter(Q(p_sestra_id=nurse.id) | Q(p_sestra_id__in=absent))
                #planned_visits = []
                #for i in absent:
                #    planned_visits |= Obisk.objects.filter(id__in=plan_list).filter(Q(p_sestra_id=nurse.id)|Q(p_sestra_id=absent.sestra_id))
                #visit_list = Obisk.objects.filter(Q(p_sestra_id=nurse.id)|Q(p_sestra_id=absent.sestra_id)).filter(~Q(id__in=plan_list)).order_by('datum')
                """SESTRA ki nadomesca je odsotna"""
                if len(current_nurse_absent) > 0:
                    absent_visits = set()
                    print("SESTRA KI NADOMESCA JE ODSOTNA ID: "+str(nurse.id))
                    for i in current_nurse_absent:
                        """GET ALL VISITS WHILE ABSENT AND FILTER BASED ON THOSE"""
                        print("DATUM ZACETEK: "+str(i.datum_zacetek)+" DATUM KONEC "+str(i.datum_konec))
                        query = Obisk.objects.filter(p_sestra_id=nurse.id,datum__range = (i.datum_zacetek, i.datum_konec)).values_list('id',flat=True)#.filter(~Q(id__in=plan_list)).values_list('id',flat=True)
                        absent_visits.update(query)
                    print("OBISKI ODSOTNE SESTRE ABSENT_VISITS")
                    #absent_visits.update(absent_ids)
                    #absent_visits.add(nurse.id)
                    print(absent_visits)
                    print(absent_ids)
                    visit_list = Obisk.objects.filter(~Q(id__in=plan_list),~Q(id__in=absent_visits),p_sestra_id=nurse.id).order_by('datum')
                    planned_visits = Obisk.objects.filter(Q(id__in=plan_list),~Q(id__in=absent_visits),p_sestra_id=nurse.id,n_sestra_id=None)
                    planned_visits |= Obisk.objects.filter(Q(id__in=plan_list), ~Q(id__in=absent_visits),
                                                          n_sestra_id=nurse.id)

                    print("PLANNED VISITS BEFORE FOR LOOP")
                    print(planned_visits)
                    for i in absent:
                        """
                        planned_visits |= Obisk.objects.filter(id__in=plan_list).filter(
                            Q(p_sestra_id=i.sestra_id)).filter(
                            datum__range=(i.datum_zacetek, i.datum_konec))
                        """
                        visit_list |= Obisk.objects.filter(Q(p_sestra_id=i.sestra_id),~Q(id__in=plan_list),datum__range=(i.datum_zacetek, i.datum_konec)).order_by(
                            'datum')

                    print("PLANIRANI OBISKI  3333: ")
                    print(plan_list)
                    print(planned_visits)
                else:
                    visit_list = Obisk.objects.filter(~Q(id__in=plan_list),p_sestra_id=nurse.id).order_by('datum')
                    planned_visits = Obisk.objects.filter(id__in=plan_list,p_sestra_id=nurse.id,n_sestra_id=None)
                    planned_visits |= Obisk.objects.filter(id__in=plan_list,n_sestra_id=nurse.id)#.filter(id__in=plan_list).order_by('datum')#filter(datum__gt=date.today())# #Okolis.objects.values_list('id','ime')
                   # planned_visits=Plan.objects.select_related().filter(planirani_obisk.id__in=plan_list).filter(planirani_obisk.p_sestra_id=nurse_id)
                    print("PLANIRANI OBISKI 4444: ")
                    print(planned_visits)
                    print("PLANIRANI OBISKI 4444 AFTER")

                #planned_visits = Obisk.objects.filter(id__in=plan_list).filter(Q(p_sestra_id=nurse.id))

                #visit_list = Obisk.objects.filter(Q(p_sestra_id=nurse.id)).filter(~Q(id__in=plan_list)).order_by('datum')

                    for i in absent:
                        print(plan_list)
                        print("NURSE: "+str(i.sestra_id)+" Start: " + str(i.datum_zacetek) + " END: " + str(i.datum_konec))
                        planned_visits |= Obisk.objects.filter(p_sestra_id=i.sestra_id,n_sestra_id=nurse.id,id__in=plan_list, datum__range=(i.datum_zacetek, i.datum_konec))

                        visit_list |= Obisk.objects.filter(Q(p_sestra_id=i.sestra_id),~Q(id__in=plan_list), datum__range=(i.datum_zacetek, i.datum_konec)).order_by('datum')

            #print("Query result")
            #add to global plan




            for i in planned_visits:
                print('planirani: '+str(i.id))

            # get the planned visit from all visits
            test_plan = Plan.objects.select_related().filter(planirani_obisk_id__in=planned_visits,datum__icontains=datum)
            #print("=======TEST PLAN=========")
            #print(test_plan)
            #print(str(datum))
            test_plan = replace_datum_type(test_plan,1)
            #global_plan=planned_visits
            global_plan = test_plan
            temp = []
           # print("<<<<<<<<<<<<<GLOBAL PLAN PRINTS>>>>>>>>>")
            for x in global_plan:
                temp.append(x.id)
                #print(x)
            global_plan = temp
            request.session['global_plan'] = global_plan

        else:

            global_plan = []
            request.session['global_plan'] = global_plan

            if not fill_in:
                print("BREZ NADOMESCANJA PLAN JE PRAZEN")

                if len(current_nurse_absent)>0:
                    absent_visits = set()
                    for i in current_nurse_absent:
                        """GET ALL VISITS WHILE ABSENT AND FILTER BASED ON THOSE"""
                        query = Obisk.objects.filter(p_sestra_id=nurse.id,datum__range = (i.datum_zacetek, i.datum_konec)).values_list('id',flat=True)#.filter(~Q(id__in=plan_list)).values_list('id',flat=True)
                        absent_visits.update(query)
                        print(absent_visits)
                    visit_list = Obisk.objects.filter(~Q(id__in=plan_list),~Q(id__in=absent_visits),p_sestra_id=nurse.id).order_by('datum')

                else:
                    visit_list = Obisk.objects.filter(~Q(id__in=plan_list),p_sestra_id=nurse.id).order_by('datum')

               # visit_list = Obisk.objects.select_related().filter(p_sestra_id=nurse.id).order_by('datum')
            else:
                # vključi obiske sestre, ki jo nadomesca
                print("NADOMESCANJE, PLAN JE PRAZEN")

                """SESTRA ki nadomesca je odsonta"""
                if len(current_nurse_absent) > 0:
                    absent_visits = set()
                    for i in current_nurse_absent:
                        """GET ALL VISITS WHILE ABSENT AND FILTER BASED ON THOSE"""
                        query = Obisk.objects.filter(p_sestra_id=nurse.id,datum__range=(i.datum_zacetek, i.datum_konec)).values_list('id',flat=True)  # .filter(~Q(id__in=plan_list)).values_list('id',flat=True)
                        absent_visits.update(query)
                        print(absent_visits)
                    visit_list = Obisk.objects.filter(~Q(id__in=plan_list), ~Q(id__in=absent_visits),p_sestra_id=nurse.id).order_by('datum')

                    for i in absent:
                       visit_list |= Obisk.objects.filter(Q(p_sestra_id=i.sestra_id),~Q(id__in=plan_list),datum__range=(i.datum_zacetek, i.datum_konec)).order_by('datum')
                else:
                    visit_list = Obisk.objects.filter(~Q(id__in=plan_list),p_sestra_id=nurse.id).order_by('datum')
                    for i in absent:
                         visit_list |= Obisk.objects.filter(Q(p_sestra_id=i.sestra_id),~Q(id__in=plan_list), datum__range=(i.datum_zacetek, i.datum_konec)).order_by('datum')
                """ 
                visit_list = Obisk.objects.select_related().filter(Q(p_sestra_id=nurse.id)).order_by('datum')
                for i in absent:
                    #print("Start: " + str(i.datum_zacetek) + " END: " + str(i.datum_konec))
                    visit_list |= Obisk.objects.select_related().filter(Q(p_sestra_id=i.sestra_id)).filter(datum__range=(i.datum_zacetek, i.datum_konec)).order_by('datum')
                """
        print("Visit list "+str(len(visit_list)))
        visit_list = replace_datum_type(visit_list,0)
    else:
        visit_list = []

   # main_nurse_id = nurse.id
    #global global_nurse_id
    request.session['global_nurse_id'] = nurse.id
    return render_to_response('ajax_plan_visit.html',{'visit_list':visit_list,'nurse':nurse.id})

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
    temp = request.session.get('global_plan')
    test_plan = Plan.objects.select_related().filter(id__in=temp)
    test_plan = replace_datum_type(test_plan, 1)
    # global_plan=planned_visits
    global_plan = test_plan
    """
    print("=========SESSIONG GET==========")
    print(global_plan)
    print("============================")
    """
    global_nurse_id = request.session.get('global_nurse_id')
    return render_to_response('ajax_already_planned.html',{'planned':global_plan,'nurse':global_nurse_id})

def plan_visit_view(request):
    if request.method == "POST":


        #current_nurse_absent = Nadomescanje.objects.filter(sestra_id=request.session.get('main_nurse')).filter(veljavno=True)
        current_nurse_absent = Nadomescanje.objects.filter(sestra_id=request.session.get('main_nurse'),veljavno=True,datum_zacetek__lte=date.today(), datum_konec__gte=date.today())

        if len(current_nurse_absent) > 0:
            # sestra je odsotna
            print("===========LOGIRANA SESTRA JE ODSOTNA=========")
            messages.error(request, 'Odsotna sestra ne more popravljati plana',extra_tags='list-group-item-danger')
            return redirect("link_plan_visit")
        visit_form = plan_visit_form(request.POST)
        plan_visit_list = request.POST.getlist('plan_list')
        my_date = request.POST['date_picker']
        print('============================================================')
        print('============AFTER FORM POST METHOD=====================')
        print(my_date)
        print('============================================================')

       # plan = None
        if my_date != '':
            datum_format = my_date.split('.')
            print("INSIDE POST: " + str(datum_format))
            datum = datum_format[2]+'-'+datum_format[1]+'-'+datum_format[0]
            print("INSIDE POST: " + datum)
            datum = datetime.strptime(datum, "%Y-%m-%d") + timedelta(hours=2)
        else:
            datum = datetime.now() + timedelta(hours=2)
            print("=================DATUM NOW============")
            print(datum)

        """TRY SESSION"""
        #global old_plan
        old_plan = request.session.get('old_plan')

       # print("OLDPLAN BEFORE: " + str(old_plan))
        #contained = [x for x in plan_visit_list if x in old_plan]
        #print("CONTAINED: "+str(contained))
        #for i in old_plan:
         #   print("old plan: "+str(i))
        if len(plan_visit_list) > 0:
            #izbrisi obiske ki odstranjene
            pk_plan = [i.split(' ',1)[0] for i in plan_visit_list]
            results = list(map(int, pk_plan))
            print("RESULTS: ")
            print(pk_plan)
            print("OLD PLAN VAL: ")
            print(old_plan)
            for i in old_plan:     #empty plan visit list =6 pk=6

                if i not in results:
                    print("Ta obisk ni v planu: "+str(i))
                    Plan.objects.get(planirani_obisk_id=str(i)).delete()
                    Obisk.objects.filter(id=str(i)).update(n_sestra_id=None)
            #shrani nove obiske
            logged_nurse = request.session.get('main_nurse')
            for i in plan_visit_list:
                obisk_id = i.split(' ', 1)[0]
                print('Plan: '+obisk_id)
                if int(obisk_id) not in old_plan:
                    print("Ta obisk ni v bazi")
                    #preveri za vikend 0-monday 4 friday
                    day = datetime.today().weekday()

                    belongs_to_nurse = Obisk.objects.get(id=obisk_id)
                    belongs_to_nurse=belongs_to_nurse.p_sestra_id
                    nadomestna_sestra = None
                    if logged_nurse != belongs_to_nurse:
                        nadomestna_sestra = logged_nurse
                    #friday
                    """
                    if day == 4:
                        plan = Plan(planirani_obisk_id=obisk_id,datum = datetime.now()+timedelta(days=3, hours=2))
                    """#el
                    if day == 5:
                        plan = Plan(planirani_obisk_id=obisk_id, datum = datetime.now() + timedelta(days=2,hours=2))
                    elif day == 6:
                        plan = Plan(planirani_obisk_id=obisk_id, datum = datetime.now() + timedelta(days=1 ,hours=2))
                    else:
                        print("==================INSIDE ELSE==============")
                        print(datum)
                        plan = Plan(planirani_obisk_id=obisk_id,datum = datum)
                    Obisk.objects.filter(id=obisk_id).update(n_sestra_id=nadomestna_sestra)

                    plan.save()
        else:
            print("======================================")
            print("=======BRISEMO PLANA======")
            print("======================================")
            logged_nurse = request.session.get('main_nurse')
            #nadomestna_sestra = None
            for i in old_plan:     #empty plan visit list =6 pk=6

                belongs_to_nurse = Obisk.objects.get(id=str(i))
                belongs_to_nurse= belongs_to_nurse.p_sestra_id
                if logged_nurse != belongs_to_nurse:
                    Obisk.objects.filter(id=str(i)).update(n_sestra_id=None)


                Plan.objects.get(planirani_obisk_id=str(i)).delete()

        messages.success(request, 'Plan je bil uspešno posodobljen', extra_tags='list-group-item-success')
        return redirect("link_plan_visit")
    else:
       visit_form = plan_visit_form()
    """
    print("GET REQUEST from view "+str( global_plan))
    for i in global_plan:
        print('View data: '+str(i))
    """
    return render(request, 'plan_visit.html', {'plan_visit_form': visit_form})