"""patronazna_sluzba_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from patronazna_sluzba_app.views import *
from django.conf import settings
from django.contrib.staticfiles import views

#from patronazna_sluzba_app.views import ZdraviloAutocomplete

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base/newStaffMember', register_medical_staff, name="link_register_medical_staff"),
    url(r'^base/controlPanel', base, name="link_control_panel"),
    # url(r'^base/newPatient', views.newPatientRegister, name="register_pacient"),
	url(r'^register/', register_patient, name='link_register_patient'),
    url(r'^base/addNursingPatient', add_nursing_patient, name="link_add_nursing"),
	url(r'^changePassword', change_password, name="link_change_password"),
    url(r'^activate/', activate),
    url(r'^listWorkTask/', list_work_task, name="link_list_work_task"),
	url(r'^workTask/', work_task_view, name="link_work_task"),
	url(r'^logout', logout_user, name="link_logout"),
	url(r'^$', index, name="link_home"),
    url(r'^medicine/search/$',search_titles),
    url(r'^patient/search/$',search_patients),
    url(r'^visit/choice/$',choose_visit_type),
    url(r'^post/$',search_post_code),
    url(r'^base/empty$', empty, name="link_empty"),
    url(r'^district/$',search_district_name),
    url(r'^visit/role/$',visit_based_on_role),
    url(r'^plan_visit', plan_visit_view, name="link_plan_visit"),
    url(r'^visit_list/$',plan_list_ajax),
    url(r'^plan_detail/$',work_task_plan),
    url(r'^illness_list/$',illness_list_view),
    url(r'^health_visitor/$',health_visitor_view),
	url(r'^static/(?P<path>.*)$', views.serve),
    url(r'^planned_list/$',ajax_added_to_plan),
    url(r'^listVisitations/', list_visitations, name="link_list_visitations"),
    url(r'^substitution/$',substitutionView,name="substitution"),
    url(r'^nurseList/$',ajax_nurse_autocomplete),
    url(r'^subNurseList/$',ajax_sub_nurse),
    url(r'^materialList/$',material_list),
    url(r'^editProfile/$',editProfileView,name='link_edit_profile'),
    url(r'^editNursing/(?P<id>[0-9]+)/$',editNursingProfileView,name='link_edit_nursing'),

]

#ADD 
urlpatterns += staticfiles_urlpatterns()


