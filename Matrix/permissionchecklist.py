#_*_coding:utf-8_*_


settings = {
	'Matrix':{
		"baseinfo_pagedataList":'查看基础资产权限',
		"baseinfo_editFun":'修改与新增基础资产权限',
		"baseinfo_deleteFun":"删除基础资产权限",
		
		"configinfo_pagedataList":'查看配置信息权限',
		"configinfo_editFun":'修改与新增配置信息权限',
		"configinfo_deleteFun":"删除配置信息权限",
		
		"platforminfo_pagedataList":'查看平台信息权限',
		"platforminfo_editFun":'修改与新增平台信息权限',
		"platforminfo_deleteFun":"删除平台信息权限",
		
		"businessinfo_pagedataList":'查看业务线信息权限',
		"businessinfo_editFun":'修改与新增业务线信息权限',
		"businessinfo_deleteFun":"删除业务线信息权限",
		
		"dnsinfo_pagedataList":'查看DNS信息权限',
		"dnsinfo_editFun":'修改与新增DNS信息权限',
		"dnsinfo_deleteFun":"删除DNS信息权限",

		"domaininfo_pagedataList":'查看Domain信息权限',
		"domaininfo_editFun":'修改与新增Domain信息权限',
		"domaininfo_deleteFun":"删除Domain信息权限",

		"assetinfo_pagedataList":'查看硬件资产信息权限',
		"assetinfo_editFun":'修改与新增硬件资产信息权限',
		"assetinfo_deleteFun":"删除硬件资产信息权限",

		"alarminfo_pagedataList":'查看监控日志',
		"alarminfo_charts":'查看监控折线图',
		"alarminfo_getalert":"告警日志显示告警弹窗",

		#以下为系统权限

	},
	'others':'others',
}

'''
auth.add_permission
Matrix.change_zabbixalertinfo
sessions.change_session

Matrix.change_configinfo
auth.delete_permission

Matrix.change_testmodels
Matrix.view_task
Matrix.delete_configinfo
admin.change_logentry
Matrix.alarminfo_charts
contenttypes.delete_contenttype

contenttypes.add_contenttype

Matrix.add_zabbixalertinfo

Matrix.change_businessunit
auth.change_group
Matrix.add_dnsinfo
Matrix.change_test
Matrix.add_domaininfo
Matrix.change_platform
Matrix.change_task_status
auth.delete_group
Matrix.xxxxx
Matrix.delete_testmodels
Matrix.delete_domaininfo
auth.change_user

Matrix.add_test
auth.add_user
Matrix.change_baseinfo
Matrix.del_test

Matrix.delete_platform
Matrix.add_platform
Matrix.add_baseinfo

contenttypes.change_contenttype
sessions.delete_session
Matrix.delete_businessunit

admin.delete_logentry
auth.add_group
Matrix.delete_zabbixalertinfo

Matrix.add_configinfo
Matrix.change_domaininfo
auth.change_permission
Matrix.change_dnsinfo
Matrix.delete_baseinfo

Matrix.alarminfo_getalert
sessions.add_session
Matrix.delete_dnsinfo
auth.delete_user
Matrix.add_businessunit

admin.add_logentry
Matrix.add_testmodels

Matrix.close_task

'''