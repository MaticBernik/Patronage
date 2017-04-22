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
from patronazna_sluzba_app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base/newStaffMember', views.medicalStaffRegister, name="register_medical_personal"),
    url(r'^base/controlPanel', views.base, name="control_panel"),
    # url(r'^base/newPatient', views.newPatientRegister, name="register_pacient"),
	url(r'^register/', views.register,name='register'),
    url(r'^base/addNursingPatient', views.addNursingPatient, name="addNursing"),
	url(r'^changePassword', views.changePassword,name="change_password"),
    url(r'^activate/', views.activate),
	url(r'^workTask/', views.workTaskForm),
	url(r'^logout', views.logout_user, name="logout"),
	url(r'^$', views.index, name="home"),
]

#ADD 
urlpatterns += staticfiles_urlpatterns()


