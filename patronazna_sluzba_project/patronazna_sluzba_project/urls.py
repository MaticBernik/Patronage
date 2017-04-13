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
from patronazna_sluzba_app import views as v
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', v.index),
	url(r'^register/', v.register,name='register'),
	url(r'^changePassword/', v.changePassword),
    url(r'^addNursingPatient/', v.addNursingPatient),
	 url(r'^workTask/', v.workTaskForm)
]

#ADD 
urlpatterns += staticfiles_urlpatterns()


