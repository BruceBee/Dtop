from django.conf.urls import patterns,include,url
from OM import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^LoadGroupInfo/', views.LoadGroupInfo),
	url(r'^LoadOMUserInfo/', views.LoadOMUserInfo),
	url(r'^ServerSync/', views.ServerSync),
	url(r'^saltHander/', views.saltHander),
	url(r'^group_add/', views.group_add),
	url(r'^group_modify/', views.group_modify),
	url(r'^group_del/', views.group_del),
	url(r'^server_add/', views.server_add),
	url(r'^server_modify/', views.server_modify),
	url(r'^server_del/', views.server_del),
	url(r'^get_serverlist_for_select/', views.get_serverlist_for_select),
	url(r'^get_all_server_list/', views.get_all_server_list),
	url(r'^get_all_groups_list/', views.get_all_groups_list),
	url(r'^download/', views.download),
]