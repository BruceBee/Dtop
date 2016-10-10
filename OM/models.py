#_*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ServerGroup(models.Model):
	servergroup_id = models.CharField(max_length=20,verbose_name='服务器组ID')
	servergroup_name = models.CharField(max_length=64,unique=True,verbose_name='服务器组名称')
	server_members = models.ManyToManyField('ServerList',blank=True,null=True,verbose_name='下属服务器')
	servergroup_memo = models.CharField(max_length=64,default='null',verbose_name='备注信息')


	class Meta:
		verbose_name = '服务器组信息表'
		verbose_name_plural = '服务器组信息表'
	def __unicode__(self):
		return self.servergroup_id


class ServerList(models.Model):
	# service_owner = models.ForeignKey('ServerGroup',default='2',verbose_name=u'服务器属组')
	server_id = models.CharField(max_length=20,blank=True,null=True,verbose_name='服务器ID')
	server_name = models.CharField(max_length=64,verbose_name='服务器主机名')
	server_ip = models.GenericIPAddressField(verbose_name='服务器IP')
	server_memo = models.CharField(max_length=64,default='null',verbose_name='备注信息')


	class Meta:
		verbose_name = '服务器信息表'
		verbose_name_plural = '服务器信息表'
	def __unicode__(self):
		return self.server_id


class CmdHistory(models.Model):
	#日志审计
	# cmd_server_group_id = models.ManyToManyField(ServerGroup,verbose_name='操作服务器组ID')
	# cmd_server_server_id = models.ManyToManyField(ServerList,verbose_name='操作服务器ID')
	client_ip = models.GenericIPAddressField(default='none',verbose_name='客户端IP')
	cmd_server_group_id = models.TextField(max_length=512,default='none',verbose_name='操作服务器组ID')
	cmd_server_server_id = models.TextField(max_length=512,default='none',verbose_name='操作服务器ID')	

	cmd_time = models.CharField(max_length=64,verbose_name='操作时间')
	cmd_user = models.CharField(max_length=64,verbose_name='操作人员')
	cmd_command = models.CharField(max_length=64,verbose_name='操作指令')

	class Meta:
		verbose_name = '操作日志表'
		verbose_name_plural = '操作日志表'
	def __unicode__(self):
		return self.cmd_command