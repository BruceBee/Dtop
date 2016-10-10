#_*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ActionLog(models.Model):

	user_id= models.CharField(max_length=20,blank=True,null=True,verbose_name='用户ID')
	user_name= models.CharField(max_length=20,blank=True,null=True,verbose_name='用户姓名')
	act_module = models.CharField(max_length=64,blank=True,null=True,verbose_name='操作模块')
	act_type = models.CharField(max_length=32,blank=True,null=True,verbose_name='操作类型')
	act_time = models.CharField(max_length=32,blank=True,null=True,verbose_name='操作时间')
	act_detail = models.TextField(max_length=256,blank=True,null=True,verbose_name='详情')

	class Meta:
		verbose_name= '系统日志表'
		verbose_name_plural ="系统日志表"

	def __unicode__(self):
		return self.user_name


class SSHLog(models.Model):
	client_ip = models.GenericIPAddressField(default='none',verbose_name='客户端IP')
	cmd_server_group_id = models.TextField(max_length=512,default='none',verbose_name='操作服务器组ID')
	cmd_server_server_id = models.TextField(max_length=512,default='none',verbose_name='操作服务器ID')	

	cmd_time = models.CharField(max_length=64,blank=True,null=True,verbose_name='操作时间')
	cmd_user = models.CharField(max_length=64,blank=True,null=True,verbose_name='操作人员')
	cmd_command = models.CharField(max_length=64,blank=True,null=True,verbose_name='操作指令')

	class Meta:
		verbose_name = '运维操作日志表'
		verbose_name_plural = '运维操作日志表'
	def __unicode__(self):
		return self.cmd_command