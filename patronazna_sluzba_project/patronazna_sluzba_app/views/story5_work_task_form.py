# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect

def work_task_form_processing(request):

    if request.method == 'POST':
        form = WorkTaskForm(request.POST)

    else:
        form = WorkTaskForm()

    return render(request, 'work_task.html', {'work_task_form': form})
