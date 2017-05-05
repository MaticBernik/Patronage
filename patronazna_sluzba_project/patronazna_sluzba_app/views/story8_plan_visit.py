# -*- coding: utf-8 -*-
# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
from datetime import date,datetime,timedelta

########################################################################
#######TEST THE FUNCTIONALITY
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
    material = Material_DN.objects.select_related().filter(delovni_nalog_id=visit_list)#get(delovni_nalog_id=visit_list)
    medicine = Zdravilo_DN.objects.select_related().filter(delovni_nalog_id=visit_list)
    print('QUERY RESULT: '+str(task_fk)+'    '+str(material)+'  '+str(medicine))
   # task = Posta.objects.all()[1:10]
    return render_to_response('ajax_task_plan.html',{'task':task_fk,'material':material,'medicine':medicine})

def plan_list_ajax(request):


    #print('Posta ajax '+post_code)
    visit_list = Obisk.objects.order_by('datum')#filter(datum__gt=date.today())# #Okolis.objects.values_list('id','ime')
    print("todays date is: "+str(date.today()))
    print("Tomorrow date is: " + str(date.today() + timedelta(days=1)))
    """
    better_list =[x[1] for x in visit_list]
    better_list_id = [x[0] for x in visit_list]
    for i in range(len(better_list)):
        better_list[i] = str(better_list_id[i])+' | '+better_list[i]
    #    print(i)
    """
    return render_to_response('ajax_plan_visit.html',{'visit_list':visit_list})

def plan_visit_view(request):
    if request.method == "POST":
        visit_form = plan_visit_form(request.POST)
        plan_visit_list = request.POST.getlist('plan_list')
        plan = None
        for i in plan_visit_list:
            print('Plan: '+i)
            plan = Plan(planirani_obisk_id=1)
            plan.save()
    else:
       visit_form = plan_visit_form()

    return render(request, 'plan_visit.html', {'plan_visit_form': visit_form})