from django.contrib import admin

# Register your models here.

from .models import *

class ActionLogAdmin(admin.ModelAdmin):
	list_display = ('user_id','user_name','act_module','act_type','act_time','act_detail')
	search_fields = ['user_id','user_name','act_module','act_type','act_time','act_detail']
	list_filter =['user_name','act_module','act_type']

class SSHLogAdmin(admin.ModelAdmin):
	list_display = ('client_ip','cmd_server_group_id','cmd_server_server_id','cmd_time','cmd_user','cmd_command',)
	search_fields = ['client_ip','cmd_user','cmd_command',]
	list_filter =['client_ip','cmd_user','cmd_command',]


admin.site.register(ActionLog,ActionLogAdmin)
admin.site.register(SSHLog,SSHLogAdmin)