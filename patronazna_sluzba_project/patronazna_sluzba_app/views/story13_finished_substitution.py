#-*- coding: utf-8 -*-
# @login_required(login_url='/')
from patronazna_sluzba_app.models import *
from patronazna_sluzba_app.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.contrib import messages
########################################################################


def finishedSubstitutionView(request):
    if request.method == "POST":
        form = SubstitutionFinishedForm(request.POST)
        nurse_absent = request.POST['nurses_absent']
        #nurse1 = Patronazna_sestra.objects.get(id=int(nurse_absent))

        nurse_substitute = request.POST['nurses_substitutes']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if nurse_substitute == nurse_absent:
            messages.error(request, 'Dvakrat ste izbrali isto sestro', extra_tags='list-group-item-danger')
            return redirect('link_sub_finished')
        #nurse2 = Patronazna_sestra.objects.get(id=int(nurse_substitute))
        """
        print("================ "+nurse_absent+" ==============")
        print("Izbrana sestra: " + str(nurse))
        print("==============================")
        """
        start_date=datumFormat(start_date)
        end_date=datumFormat(end_date)

        q = Nadomescanje.objects.filter(veljavno=True,sestra_id=int(nurse_absent),nadomestna_sestra=int(nurse_substitute),datum_zacetek=start_date,datum_konec=end_date).update(veljavno=False)
        print(q)
        if q<1:
            messages.warning(request, 'Nadomeščanje z izbranimi parametri ne obstaja!', extra_tags='list-group-item-warning')
            return redirect('link_sub_finished')

        #for i in q:
         #   print(i.veljavno)
        print("========UPDATED=======")
        messages.success(request, 'Uspešno zaključeno nadomeščanje', extra_tags='list-group-item-success')
        return redirect('link_sub_finished')
    else:

        form = SubstitutionFinishedForm()

    sub_query = Nadomescanje.objects.select_related().filter(veljavno=True)

    return render(request, 'nurse_sub_finished.html', {'substitution_form': form,"nadomescanje_list":sub_query})

def datumFormat(datum):
    if datum != '':
        datum_format = datum.split('.')
        datum = datum_format[2] + '-' + datum_format[1] + '-' + datum_format[0]
    else:
        datum = datetime.now().date()
    return  datum