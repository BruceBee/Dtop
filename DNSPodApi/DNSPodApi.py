#coding=utf-8
import os,django,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtop.settings")# project_name 项目名称
django.setup()
import json,sys,os,django
import urllib2,datetime,time
import redis
import commands

# os.environ['DJANGO_SETTINGS_MODULE'] = 'dtop.settings'
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print BASE_DIR
sys.path.append(BASE_DIR)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'dtop.settings'
from Matrix import models
# os.environ['DJANGO_SETTINGS_MODULE'] = 'dtop.settings'
# django.setup()

def getmessage():

	LOGIN_TOKEN='1111111111111'
	#这里根据实际情况修改LOGIN_TOKEN
	# domain_id = '28639253'
	# domain_remark = '备注内容01'
	
	#设置domain的备注
	# CMD ="curl -sX POST https://dnsapi.cn/Domain.Remark -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id="+domain_id+"&remark="+domain_remark+"'"
	
	#获取domain的信息列表
	# CMD ="curl -sX POST https://dnsapi.cn/Domain.List -d 'login_token="+LOGIN_TOKEN+"&format=json'"
	
	#设置domain的状态
	# CMD ="curl -sX POST https://dnsapi.cn/Domain.Status  -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id=45640100status=disable'"
	
	#得到domain的信息
	# CMD ="curl -sX POST https://dnsapi.cn/Record.Status  -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id=45640100&record_id=227432544&remark=中文&status=enable'"
	# test的domain_id：45640100
	# 1.1.1.1的record_id:227432544
	
	# curl -X POST https://dnsapi.cn/Domain.Remark -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id=2059079&remark=这个域名需要备注一下'
	
	#获取指定record的信息
	# CMD ="curl -sX POST https://dnsapi.cn/Record.Info  -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id=28639253&record_id=132339978'"

	#设置指定record的remark值
	# CMD ="curl -sX POST https://dnsapi.cn/Record.Remark  -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id=28639253&record_id=132339978&remark=test'"

	# 删除record信息
	# CMD ="curl -sX POST https://dnsapi.cn/Record.Remove  -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id=45640100&record_id=227432544'"

	#删除domain信息
	# CMD ="curl -sX POST https://dnsapi.cn/Domain.Remove  -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id=45640100'"

	#获取允许的线路类型
	CMD ="curl -sX POST https://dnsapi.cn/Record.Line  -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_grade=D_Free&domain_id=12154450'"


	raw_data=commands.getoutput(CMD)
	req=json.loads(raw_data)
	return req

if __name__ == '__main__':

	aa = getmessage()
	# print aa['status']['code']
	if aa['status']['code'] == '1':
		# print '修改成功'
		print aa
	else:
		print aa['status']['code'],aa['status']['message']





