from django.contrib import admin

# Register your models here.
from django import forms
from .models import *

class ServerGroupAdmin(admin.ModelAdmin):
	list_display = ('servergroup_id','servergroup_name','servergroup_memo')
	search_fields = ['servergroup_id','servergroup_name','server_members','servergroup_memo']
	list_filter =['servergroup_id','servergroup_name',]

class ServerListAdmin(admin.ModelAdmin):
	list_display = ('id','server_id','server_name','server_ip','server_memo')
	search_fields = ['server_id','server_name','server_ip','server_memo']
	list_filter =['server_id','server_name','server_ip','server_memo']

class CmdHistoryAdmin(admin.ModelAdmin):
	list_display = ('client_ip','cmd_server_group_id','cmd_server_server_id','cmd_time','cmd_user','cmd_command',)
	search_fields = ['client_ip','cmd_user','cmd_command',]
	list_filter =['client_ip','cmd_user','cmd_command',]



admin.site.register(ServerGroup,ServerGroupAdmin)
admin.site.register(ServerList,ServerListAdmin)
admin.site.register(CmdHistory,CmdHistoryAdmin)