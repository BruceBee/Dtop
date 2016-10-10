from django.conf.urls import patterns,include,url
from Log import views
urlpatterns = [
	url(r'^$', views.test),
]