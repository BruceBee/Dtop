#_*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#基础信息表
class BaseInfo(models.Model):
	sid = models.CharField(max_length=40,unique=True,verbose_name=u'资源ID')
	hostname = models.CharField(max_length=30,verbose_name=u'主机名称')
	isp = models.ForeignKey('Platform',max_length=20,blank=True,null=True,verbose_name=u'服务提供商')
	# isp = models.CharField(max_length=30,null=True,blank=True,verbose_name=u'服务提供商')
	status_type=(
		(u'在线',u'在线'),
        (u'停用',u'停用'),
        (u'测试',u'测试'),
        (u'备用',u'备用'),
        (u'其他',u'其他')
		)
	status = models.CharField(max_length=20,choices=status_type,default=u'在线',verbose_name=u'资产状态')
	# status = models.CharField(max_length=20,verbose_name=u'资产状态')
	# create_date = models.DateTimeField(verbose_name=u'创建日期',blank=True,null=True)
	create_date = models.CharField(max_length=64,verbose_name=u'创建日期',blank=True,null=True)
	# expire_date = models.DateTimeField(verbose_name=u'到期日期',blank=True,null=True)
	expire_date = models.CharField(max_length=64,verbose_name=u'到期日期',blank=True,null=True)
	admin = models.CharField(max_length=64,null=True,blank=True,verbose_name=u'资产管理员')
	business_unit = models.ManyToManyField('BusinessUnit',null=True,blank=True,verbose_name=u'所属业务线')
	# business_unit = models.CharField(max_length=64,null=True,blank=True,verbose_name=u'所属业务线')

	# business_unit = models.ManyToManyField('BusinessUnit',through='ConfForBase',verbose_name=u'所属业务线')
	tags = models.CharField(max_length=64, blank=True,verbose_name=u'标签')
	memo = models.CharField(max_length=256,blank=True,verbose_name=u'备注信息')

	class Meta:
		verbose_name = '基础资产表'
		verbose_name_plural = '基础资产表'
		permissions = (
			("baseinfo_pagedataList",'查看基础资产权限'),
			("baseinfo_editFun",'修改与新增基础资产权限'),
			("baseinfo_deleteFun","删除基础资产权限"),
			)

	def __unicode__(self):
		return self.hostname


#配置信息表
class ConfigInfo(models.Model):
	baseid = models.ForeignKey('BaseInfo',verbose_name=u'资源ID')
	# baseid = models.CharField(max_length=64,verbose_name=u'资源ID')
	cpu_info = models.CharField(max_length=64,null=True,blank=True,verbose_name=u'CPU信息')
	men_info = models.CharField(max_length=64,null=True,blank=True,verbose_name=u'内存信息')
	disk_info = models.CharField(max_length=64,null=True,blank=True,verbose_name=u'硬盘信息')
	os = models.CharField(max_length=20,null=True,blank=True,verbose_name=u'操作系统')
	public_ip = models.CharField(max_length=128,null=True,blank=True,verbose_name=u'公网IP')
	private_ip = models.CharField(max_length=128,unique=True,verbose_name=u'私网IP')
	mgmt_ip = models.CharField(u'管理IP',max_length=128,null=True,blank=True)
	memo = models.CharField(max_length=256,null=True,blank=True,verbose_name=u'备注信息')
	class Meta:
		verbose_name = u"配置信息表"
		verbose_name_plural = u"配置信息表"
		# unique_together = ("public_ip",'private_ip')
		permissions = (
			("configinfo_pagedataList",'查看配置信息权限'),
			("configinfo_editFun",'修改与新增配置信息权限'),
			("configinfo_deleteFun","删除配置信息权限"),
			)

	def __unicode__(self):
		return self.baseid.hostname



# class ConfForBase(models.Model):#自定义的多对多表
# 	base = models.ForeignKey(BaseInfo)
# 	config = models.ForeignKey(ConfigInfo)



#平台信息表
class Platform(models.Model):
    name = models.CharField(max_length=32,verbose_name=u'平台名称')
    domain = models.CharField(max_length=64,verbose_name=u'平台域名',default=None,blank=True,null=True)
    url = models.CharField(max_length=64,verbose_name=u'URL地址',default=None,blank=True,null=True)
    phonecall = models.CharField(max_length=32,verbose_name=u'平台电话')
    memo = models.CharField(max_length=64,verbose_name=u'备注信息')

    class Meta:
        verbose_name = '云平台'
        verbose_name_plural = '云平台'
        permissions = (
			("platforminfo_pagedataList",'查看平台信息权限'),
			("platforminfo_editFun",'修改与新增平台信息权限'),
			("platforminfo_deleteFun","删除平台信息权限"),
			)
    def __unicode__(self):
    	return self.name

#业务线信息表
class BusinessUnit(models.Model):
    name = models.CharField(max_length=64,verbose_name=u'业务线名称')
    admin = models.CharField(max_length=64,verbose_name=u'业务线所属管理员')
    memo = models.CharField(max_length=64,verbose_name=u'备注信息')

    class Meta:
        verbose_name ='业务线'
        verbose_name_plural = '业务线'
        permissions = (
			("businessinfo_pagedataList",'查看业务线信息权限'),
			("businessinfo_editFun",'修改与新增业务线信息权限'),
			("businessinfo_deleteFun","删除业务线信息权限"),
			)
    def __unicode__(self):
    	return self.name


class DomainInfo(models.Model):
	domain_id = models.CharField(max_length=20,unique=True,verbose_name='域名ID')
	domain_status = models.CharField(max_length=64,verbose_name='域名状态')
	domain_name = models.CharField(max_length=64,verbose_name='域名')
	domain_records = models.CharField(max_length=256,verbose_name='域名记录条数')
	domain_remark = models.CharField(max_length=64,blank=True,default=None,verbose_name='域名备注')
	domain_grade = models.CharField(max_length=64,blank=True,default=None,verbose_name='域名套餐等级')


	class Meta:
		verbose_name = '域名信息表'
		verbose_name_plural = '域名信息表'
		permissions = (
			("domaininfo_pagedataList",'查看Domain信息权限'),
			("domaininfo_editFun",'修改与新增Domain信息权限'),
			("domaininfo_deleteFun","删除Domain信息权限"),
			)

	def __unicode__(self):
		return self.domain_name

class DnsInfo(models.Model):
	Domain_name = models.ForeignKey('DomainInfo',max_length=64,default=None,verbose_name='所属域名',)
	dns_id = models.CharField(max_length=64,unique=True,default=None,verbose_name=u'DNS ID号',)
	dns_name = models.CharField(max_length=64,default=None,verbose_name='子域名（主机记录）',)
	dns_type = models.CharField(max_length=64,blank=True,null=True,verbose_name='记录类型',)
	dns_line = models.CharField(max_length=64,blank=True,null=True,verbose_name='链路类型',)
	dns_value = models.CharField(max_length=64,blank=True,null=True,verbose_name='记录值',)
	dns_weight = models.CharField(max_length=64,blank=True,null=True,verbose_name='权重',)
	dns_mx = models.CharField(max_length=64,blank=True,null=True,default=None,verbose_name='MX优先级',)
	dns_ttl = models.IntegerField(default=600,blank=True,null=True,verbose_name='ttl',)
	#is_enabled = models.IntegerField(default=1,blank=True,null=True,verbose_name='启用状态值',)
	enabled_type=(
		('1',u'启用'),
        ('0',u'未启用')
		)
	dns_enabled = models.CharField(max_length=64,choices=enabled_type,default='1',verbose_name='状态')
	# domain_id = models.IntegerField(default=1)
	
	dns_remark = models.CharField(max_length=64,blank=True,default=None,verbose_name='备注',)
	dns_updated_on = models.CharField(max_length=64,blank=True,default=None,verbose_name='更新时间',)
	dnsop = models.CharField(max_length=64,default=None,verbose_name='操作人员',)

	class Meta:
		verbose_name = 'DNS信息表'
		verbose_name_plural = 'DNS信息表'
		permissions = (
			("dnsinfo_pagedataList",'查看DNS信息权限'),
			("dnsinfo_editFun",'修改与新增DNS信息权限'),
			("dnsinfo_deleteFun","删除DNS信息权限"),
			)

	def __unicode__(self):
		return self.dns_id


class DomainRecordLine(models.Model):
	Domain_id = models.CharField(max_length=64,verbose_name='主域名')
	# Domain_name = models.CharField(max_length=64,verbose_name='根域名')
	# Domain_grade = models.CharField(max_length=64,verbose_name='域名套餐')
	record_lines_ids = models.CharField(max_length=64,verbose_name='线路名称')
	record_zone = models.CharField(max_length=256,blank=True,null=True,verbose_name='线路覆盖区域')
	record_line_id  = models.CharField(max_length=64,verbose_name='线路ID')


	class Meta:
		verbose_name = '域名记录可选线路表'
		verbose_name_plural = '域名记录可选线路表'
		unique_together = ("Domain_id","record_lines_ids")
		# permissions = (
		# 	("dnsinfo_pagedataList",'查看DNS信息权限'),
		# 	("dnsinfo_editFun",'修改与新增DNS信息权限'),
		# 	("dnsinfo_deleteFun","删除DNS信息权限"),
		# 	)

	def __unicode__(self):
		return self.record_lines_ids

class DomainRecordType(models.Model):
	domain_name = models.CharField(max_length=32,default=None,verbose_name='主域名')
	domain_grade = models.CharField(max_length=32,verbose_name='域名套餐等级')
	record_type = models.CharField(max_length=256,verbose_name='记录可选类型')
	class Meta:
		verbose_name = '域名记录可选类型表'
		verbose_name_plural = '域名记录可选类型表'

	def __unicode__(self):
		return self.domain_grade




# class Test(models.Model):
# 	test_name = models.CharField(max_length=20)
# 	test_age = models.IntegerField()
# 	test_add = models.CharField(max_length=20)
		


class ZabbixAlertInfo(models.Model):
	eventid = models.CharField(max_length=20,verbose_name='事件ID')
	alerttime = models.CharField(max_length=64,verbose_name='告警时间')
	subject = models.CharField(max_length=128,verbose_name='告警主题')
	message = models.CharField(max_length=256,verbose_name='告警详情')
	sendto = models.CharField(max_length=64,verbose_name='收件人')
	status = models.CharField(max_length=20,verbose_name='告警状态')

	class Meta:
		verbose_name = 'zabbix告警信息表'
		verbose_name_plural = 'zabbix告警信息表'
		permissions = (
			("alarminfo_pagedataList",'查看监控日志'),
			("alarminfo_charts",'查看监控折线图'),
			("alarminfo_getalert","告警日志显示告警弹窗"),
			)

	def __unicode__(self):
		return self.eventid



class Asset(models.Model):
	device_id = models.CharField(max_length=20,unique=True,verbose_name='资产编号')
	device_type_choices=(
		('0',u'主机'),
        ('1',u'显示器'),
        ('2',u'笔记本'),
        ('3',u'iPad/iPod'),
        ('4',u'iPhone'),
        ('安卓手机',u'安卓手机'),
        ('6',u'windows Phone')
		)
	device_type=models.CharField(max_length=64,blank=True,default=None,verbose_name='设备类型')
	device_model = models.CharField(max_length=20,blank=True,default=None,verbose_name='设备型号')
	device_status_choices=(
		('0',u'空闲'),
        ('1',u'使用中'),
        ('2',u'故障'),
        ('3',u'损坏'),
        ('4',u'其他')
		)
	device_status=models.CharField(max_length=20,blank=True,default=None,verbose_name='设备状态')
	device_dept = models.CharField(max_length=20,blank=True,default=None,verbose_name='使用部门')
	device_user = models.CharField(max_length=20,blank=True,default=None,verbose_name='使用人')
	device_memo = models.CharField(max_length=64,blank=True,default=None,verbose_name='备注信息')

	class Meta:
		verbose_name = '硬件资产表'
		verbose_name_plural = '硬件资产表'
		permissions = (
			("assetinfo_pagedataList",'查看硬件资产信息权限'),
			("assetinfo_editFun",'修改与新增硬件资产信息权限'),
			("assetinfo_deleteFun","删除硬件资产信息权限"),
			)

	def __unicode__(self):
		return self.device_id

class Testmodels(models.Model):
	testid = models.CharField(max_length=20,verbose_name='ID')
	name = models.CharField(max_length=20,verbose_name='name')
	age = models.IntegerField(verbose_name='年龄')

	class Meta:
		permissions = (
            ("add_test", "新增数据"),
            ("change_test", "修改数据"),
            ("del_test", "删除数据"),
        )






