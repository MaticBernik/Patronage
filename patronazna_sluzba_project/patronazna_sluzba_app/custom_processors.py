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
        view_substitutes_arr = ["link_empty", "Nadomeščanje", "v_subs", "glyphicon-th-list" ]
        view_visitations_arr = ["link_empty", "Pregled obiskov", "v_visits", "glyphicon-th-list" ]
        view_work_tasks_arr = ["link_empty", "Pregled delovnih nalogov", "v_wrk_tsk", "glyphicon-th-list" ]

        # adapt the list based on user role and task privleges
        if is_admin(user):
            role="Admin"
            link_list = [control_panel_arr, arr_add_medical_staff, change_password_arr]
        elif is_doctor(user):
            role="Zdravnik"
            link_list = [control_panel_arr, create_work_task_arr, view_visitations_arr, view_substitutes_arr, change_password_arr]
        elif is_leader_ps(user):
            role="Vodja PS"
            link_list = [control_panel_arr, create_work_task_arr, view_visitations_arr, view_substitutes_arr, change_password_arr]
        elif is_nurse(user):
            role="medicinska sestra"
            link_list = [control_panel_arr, create_work_task_arr, view_visitations_arr, view_substitutes_arr, change_password_arr]
        elif is_coworker(user):
            role="Sodelavec"
            link_list = [control_panel_arr, view_visitations_arr, view_substitutes_arr, change_password_arr ]
        else:
            role="Pacient"
            link_list = [control_panel_arr, view_visitations_arr, add_nursing_patient_arr, change_password_arr ]
        
        oskrbovanci = None

        if Pacient.objects.filter(uporabniski_profil=user).exists():
            pacient = Pacient.objects.get(uporabniski_profil=user)
            oskrbovanci = Pacient.objects.filter(skrbnistvo=pacient)
        
        return {'link_list': link_list, 'role': role, 'oskrbovanci': oskrbovanci}

    else:
        return {}