#_*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#事项总表
class Items(models.Model):
	items_status_type = (
		(u'未开始',u'未开始'),
		(u'进行中',u'进行中'),
		(u'逾期/未开始',u'逾期/未开始'),
		(u'逾期/进行中',u'逾期/进行中'),
		(u'逾期/已结束',u'逾期/已结束'),
		(u'已结束',u'已结束'),
		) 
	items_status = models.CharField(max_length=20,choices=items_status_type,verbose_name=u'事项状态')
	items_title = models.CharField(max_length=64,verbose_name='事项标题')
	items_content = models.TextField(max_length=128,verbose_name='事项说明')
	items_starter = models.CharField(max_length=64,verbose_name='发起人')
	items_owner = models.CharField(max_length=64,verbose_name='主办人')
	items_relater = models.CharField(max_length=256,verbose_name='知会人')
	create_time = models.CharField(max_length=64,verbose_name='事项创建时间')
	finish_time = models.CharField(max_length=64,blank=True,null=True,verbose_name='事项结束时间')
	finish_info = models.TextField(max_length=256,default="",blank=True,null=True,verbose_name='事项结束意见')
	start_time = models.CharField(max_length=64,verbose_name='事项计划开始时间')
	end_time = models.CharField(max_length=64,verbose_name='事项计划结束时间')
	items_rate = models.CharField(max_length=5,default=0,verbose_name='事项完成百分百')

	class Meta:
		verbose_name = '事项总表'
		verbose_name_plural = '事项总表'

	def __unicode__(self):
		return self.items_title

#处理详情表
class HandleDetail(models.Model):
	items_id = models.ForeignKey(Items,verbose_name=u'事项ID')
	handle_time = models.CharField(max_length=64,verbose_name='事项处理时间')
	handle_user = models.CharField(max_length=64,verbose_name='事项处理人员')
	handle_info = models.TextField(max_length=256,verbose_name='事项处理意见')

	class Meta:
		verbose_name = '处理详情表'
		verbose_name_plural = '处理详情表'

	def __unicode__(self):
		return self.items_id.items_title



