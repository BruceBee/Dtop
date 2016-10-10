"""dtop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns,include,url
from django.contrib import admin
from django.contrib.auth.views import login,logout
from django.views.generic.base import RedirectView
# from Matrix.views import TestView
import Matrix.views

urlpatterns = [
    url(r'^V/', admin.site.urls),
    url(r'^$', Matrix.views.login),
    url(r'^favicon\.ico$', Matrix.views.favicon),
    url(r'^auth$', Matrix.views.auth),
    url(r'^auth\.html$', Matrix.views.login),
    url(r'^accounts/login/', Matrix.views.login),
    url(r'^logout\.html$', logout, {'template_name': 'logout.html'}),
    #test
    # url(r'^test/', TestView.as_view(template_name='test.html')),
    #apps
    url(r'^home/', Matrix.views.index),
    url(r'^dns/', Matrix.views.index),
    url(r'^link/', Matrix.views.index),
    url(r'^alarm/', Matrix.views.index),
    url(r'^info/', Matrix.views.index),
    url(r'^preview/', Matrix.views.index),
    url(r'^auto/', Matrix.views.index),
    url(r'^auth/', Matrix.views.index),
    url(r'^asset/', Matrix.views.index),
    # url(r'^om/', Matrix.views.index),
    #datas
    # url(r'^admin_data/', Matrix.views.admin_data),
    url(r'^auto_data/', Matrix.views.auto_data),
    url(r'^dns_data/', Matrix.views.dns_data),
    url(r'^base_data/', Matrix.views.base_data),
    url(r'^alarm_data/', Matrix.views.alarm_data),
    url(r'^auth_data/',Matrix.views.auth_data,name='auth_data'),
    url(r'^asset_data/', Matrix.views.asset_data),
    url(r'^loadDashboard/', Matrix.views.loadDashboard),
    url(r'^BulidData/', Matrix.views.BulidData),
    url(r'^download/(\w+)*/$', Matrix.views.download),
    # url(r'^download/(\d{1,2})/$', Matrix.views.download),

    # url(r'^.*/', Matrix.views.err404),

    # url(r'^om/', Matrix.views.om),

    url(r'^OM/',include('OM.urls')),
    url(r'^Log/',include('Log.urls')),
    url(r'^em/',include('EventManagement.urls')),


    #paths
    #url(r'^images/(?P<path>.*)$','django.views.static.serve',{'document_root':'/var/www/html/dtop/static/matrix/images'}),
    #url(r'^css/(?P<path>.*)$','django.views.static.serve',{'document_root':'/var/www/html/dtop/static/matrix/css'}),
    #url(r'^js/(?P<path>.*)$','django.views.static.serve',{'document_root':'/var/www/html/dtop/static/matrix/js'}),
    #url(r'^font-awesome/(?P<path>.*)$','django.views.static.serve',{'document_root':'/var/www/html/dtop/static/matrix/font-awesome'}),
    #url(r'^img/(?P<path>.*)$','django.views.static.serve',{'document_root':'/var/www/html/dtop/static/matrix/img'}),
    #url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':'/var/www/html/dtop/static'}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
