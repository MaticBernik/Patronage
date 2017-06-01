# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, password_validation, update_session_auth_hash
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from patronazna_sluzba_app.forms import *
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.views.story3_login_logout_system import *

def navbar_list_processor(request):

    user=request.user
    # print(user)
    # print(user.is_authenticated())

    if(user.is_authenticated()):

        link_list = []

        control_panel_arr = ["link_control_panel", "Pregledna plošča", "ctrl_panel", "glyphicon-home"]
        # possible functionalities
        add_medical_staff_arr = ["link_register_medical_staff", "Dodaj zdravstveno osebje", "add_medic", "glyphicon-plus" ]
        add_nursing_patient_arr = ["link_add_nursing", "Dodajte oskrbovano osebo", "add_nursing", "glyphicon-plus" ]
        change_password_arr = ["link_change_password", "Sprememba gesla", "chng_pass", "glyphicon-erase" ]
        
        create_work_task_arr = ["link_work_task", "Ustvarite delovni nalog", "c_wrk_tsk", "glyphicon-file" ]
        create_substitution_arr = ["substitution", "Ustvarite nadomeščanje", "c_subs", "glyphicon-retweet" ]
        end_substitution_arr = ["link_sub_finished", "Zaključek nadomeščanja", "c_end_subs", "glyphicon-ok-circle" ]


        visitations_nurse_data_arr = ["link_visitations_nurse_data", "Vnos podatkov o obisku", "v_nrs_visits_data", "glyphicon-pencil" ] 


        view_substitutes_arr = ["link_empty", "Nadomeščanje", "v_subs", "glyphicon-th-list" ]
        view_visitations_arr = ["link_list_visitations", "Pregled obiskov", "v_visits", "glyphicon-th-list" ] 
        view_work_tasks_arr = ["link_list_work_task", "Pregled delovnih nalogov", "v_wrk_tsk", "glyphicon-th-list" ]
        
        visitation_planning_arr = ["link_plan_visit", "Planiranje obiskov", "v_plan_visits", "  glyphicon glyphicon-calendar" ]
        
        # adapt the list based on user role and task privleges
        dropdowns_list = []

        dropdown_worktasks = []
        dropdown_visitations = []
        dropdown_substitutions = []
        dropdown_settings = []
        dropdown_staff_management = []
        

        if is_admin(user):
            role="Admin"
            link_list = [control_panel_arr]
            dropdown_settings.append(change_password_arr)
            dropdown_staff_management.append(add_medical_staff_arr)
        elif is_doctor(user):
            role="Zdravnik"
            link_list = [control_panel_arr]
            dropdown_worktasks.append(create_work_task_arr)
            dropdown_worktasks.append(view_work_tasks_arr)
            dropdown_visitations.append(view_visitations_arr)
            dropdown_settings.append(change_password_arr)
        elif is_leader_ps(user):
            role="Vodja PS"
            link_list = [control_panel_arr]
            dropdown_worktasks.append(create_work_task_arr)
            dropdown_worktasks.append(view_work_tasks_arr)
            dropdown_visitations.append(view_visitations_arr)
            dropdown_substitutions.append(create_substitution_arr)
            dropdown_substitutions.append(end_substitution_arr)
            dropdown_settings.append(change_password_arr)
        elif is_nurse(user):
            role="medicinska sestra"
            link_list = [control_panel_arr]
            dropdown_worktasks.append(view_work_tasks_arr)
            dropdown_visitations.append(view_visitations_arr)
            dropdown_visitations.append(visitation_planning_arr)
            dropdown_visitations.append(visitations_nurse_data_arr)
            dropdown_settings.append(change_password_arr)
        elif is_coworker(user):
            role="Sodelavec"
            link_list = [control_panel_arr, change_password_arr ]
        else:
            role="Pacient"
            link_list = [control_panel_arr, add_nursing_patient_arr, change_password_arr ]
        
        oskrbovanci = None

        if(len(dropdown_worktasks) > 0 ):
            dropdowns_list.append([dropdown_worktasks, "Delovni nalogi", "glyphicon-book"])

        if(len(dropdown_visitations) > 0 ):
            dropdowns_list.append([dropdown_visitations, "Obiski", "glyphicon-dashboard"])

        if(len(dropdown_substitutions) > 0 ):
            dropdowns_list.append([dropdown_substitutions, "Nadomeščanja", "glyphicon-random"])

        if(len(dropdown_staff_management) > 0 ):
            dropdowns_list.append([dropdown_staff_management, "Osebje", "glyphicon-paperclip"])

        if(len(dropdown_settings) > 0 ):
            dropdowns_list.append([dropdown_settings, "Nastavitve", "glyphicon-cog"]) 


        if Pacient.objects.filter(uporabniski_profil=user).exists():
            print("User exits in patient filters")
            pacient = Pacient.objects.get(uporabniski_profil=user)
            print(pacient.uporabniski_profil.first_name)
            oskrbovanci = Pacient.objects.filter(skrbnistvo=pacient)
            print(oskrbovanci)
            print(pacient.st_kartice)
        else:
            print("user missing in patient filters")
        
        return {'dropdowns_list': dropdowns_list,'link_list': link_list, 'role': role, 'oskrbovanci_pacienta': oskrbovanci}

    else:
        return {}