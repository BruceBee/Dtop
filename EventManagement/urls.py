from django.conf.urls import patterns,include,url
from EventManagement import views
urlpatterns = [
	url(r'^$', views.index),
	url(r'^detail/(\w+)*/$', views.detail),
	url(r'^overview/', views.overview),
	url(r'^Item_list/(\w+)*/$', views.Item_list),
	url(r'^Items_handle/', views.Items_handle),

	url(r'^Items_notice/', views.Items_notice),
	url(r'^Notice_detail/(\w+)*/$', views.Notice_detail),

	url(r'^AddItems/', views.AddItems),
	url(r'^TakeItems/', views.TakeItems),
	url(r'^Item_init/', views.Item_init),
	url(r'^DelItems/', views.DelItems),
]