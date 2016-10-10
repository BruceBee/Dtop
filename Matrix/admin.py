from django.contrib import admin

# Register your models here.

from django import forms
from .models import *


class BaseAdmin(admin.ModelAdmin):
	list_display = ('sid','hostname','isp','status','create_date','expire_date','admin','tags','memo',)
	search_fields = ['sid','hostname','isp','status','business_unit',]
	list_filter =['sid','hostname','isp','status','business_unit',]
	# list_display = ('sid','hostname','isp','status','create_date','expire_date','admin','business_unit','tags','memo',)
	# search_fields = ['sid','hostname','isp','status','business_unit',]
	# list_filter =['sid','hostname','isp','status','business_unit',]

class ConfigAdmin(admin.ModelAdmin):
	list_display = ('baseid','cpu_info','men_info','disk_info','os','public_ip','private_ip','mgmt_ip',)
	search_fields = ['baseid','cpu_info','men_info','disk_info','os','public_ip','private_ip','mgmt_ip',]
	list_filter =['baseid','cpu_info','men_info','disk_info','os',]

class PlatAdmin(admin.ModelAdmin):
	list_display = ('name','domain','url','phonecall','memo',)
	search_fields = ['name']
	list_filter = ['name']

class BusinessAdmin(admin.ModelAdmin):
	list_display = ('name','admin','memo',)
	search_fields = ['name','admin','memo',]
	list_filter = ['name','admin','memo',]

class DomainAdmin(admin.ModelAdmin):
	list_display = ('domain_id','domain_name','domain_status','domain_records','domain_grade','domain_remark',)
	search_fields = ['domain_id','domain_name','domain_status','domain_records','domain_grade','domain_remark',]
	list_filter = ['domain_id','domain_name','domain_grade','domain_status',]

class DnsAdmin(admin.ModelAdmin):
	list_display = ('Domain_name','dns_id','dns_name','dns_value','dns_weight','dns_mx','dns_ttl','dns_enabled','dns_updated_on','dnsop',)
	search_fields = ['Domain_name','dns_id',]
	list_filter = ['Domain_name','dns_id',]

class DomainRecordLineAdmin(admin.ModelAdmin):
	list_display = ('Domain_id','record_lines_ids','record_zone','record_line_id',)
	search_fields = ['Domain_id','record_lines_ids','record_zone','record_line_id',]
	list_filter = ['Domain_id','record_lines_ids',]

class DomainRecordTypeAdmin(admin.ModelAdmin):
	list_display = ('domain_name','domain_grade','record_type',)
	search_fields = ['domain_name','domain_grade','record_type',]
	list_filter = ['domain_name','domain_grade','record_type',]


class ZabbixInfoAdmin(admin.ModelAdmin):
	list_display = ('eventid','alerttime','subject','message','sendto','status',)
	search_fields = ['eventid','alerttime','subject','message','sendto','status',]
	list_filter = ['eventid','alerttime','subject','message','sendto','status',]


class AssetAdmin(admin.ModelAdmin):
	list_display = ('device_id','device_model','device_status','device_dept','device_user','device_memo',)
	search_fields = ['device_id','device_model','device_status','device_dept','device_user','device_memo',]
	list_filter = ['device_id','device_model','device_status','device_dept','device_user','device_memo',]

admin.site.register(BaseInfo,BaseAdmin)
admin.site.register(ConfigInfo,ConfigAdmin)
admin.site.register(Platform,PlatAdmin)
admin.site.register(BusinessUnit,BusinessAdmin)
admin.site.register(DnsInfo,DnsAdmin)
admin.site.register(DomainInfo,DomainAdmin)
admin.site.register(DomainRecordLine,DomainRecordLineAdmin)
admin.site.register(DomainRecordType,DomainRecordTypeAdmin)
admin.site.register(ZabbixAlertInfo,ZabbixInfoAdmin)
admin.site.register(Asset,AssetAdmin)