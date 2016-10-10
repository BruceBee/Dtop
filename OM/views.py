#-*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,render_to_response,HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,Group,Permission
from django.http import StreamingHttpResponse
from OM import models
from dtop import settings
# from Matrix import views
# Create your views here.
from OM import models,saltHandle
from saltHandle import test,saltrun,rpyc_run,rpyc_server
from datetime import date
import salt.client
import socket
import rpyc
import json
import time,datetime
import os,statvfs
# from Log import models

from Log import logHandle
from DataDownload import BulidExcel
import om_excel
import urllib2
import urllib
from download.core import FileHandle


def index(request):
	true_name = request.user.first_name
	return render(request,'om/OMindex.html',{'apps':settings.apps,'true_name':true_name,'Used':settings.Used,'Size':settings.Size,'Percent':settings.Percent,})


def LoadGroupInfo(request):
	servergroup_obj = models.ServerGroup.objects.all()
	ret = ""
	for i in servergroup_obj:
		ser_id = i.servergroup_id
		ser_name = i.servergroup_name
		ret+=ser_id+','+ser_name+';'
	return HttpResponse(ret)
	# return HttpResponse('<h2>this is a test HttpResponse</h2>')

def LoadOMUserInfo(request):
	serveruser_obj = models.ServerList.objects.all()
	ret = ""
	for i in serveruser_obj:
		ser_id = i.server_id
		ser_name = i.server_name
		ser_ip = i.server_ip
		ser_memo = i.server_memo
		ret+=ser_id+','+ser_ip+','+ser_memo+';'
	return HttpResponse(ret)


def group_add(request):
	# ret =logHandle.ActionRecord(user_name=request.user.first_name,act_detail='login')
	# return HttpResponse(ret)
	if request.method == "POST":
		group_id = request.POST['group_id']
		group_name = request.POST['group_name']
		group_members = request.POST['members']
		if group_members =="":
			return HttpResponse('下属服务器为空,添加失败')
		try:
			members_list = group_members.split(";")
			group_obj = models.ServerGroup.objects.create(servergroup_id=group_id,servergroup_name=group_name)
			# members_list = group_members.split(";")
			for i in range(len(members_list)):
				members_obj = models.ServerList.objects.filter(server_name=members_list[i])
				group_obj.server_members.add(*members_obj)

			return HttpResponse('1')
		except Exception, e:
			return HttpResponse(e)
		else:
			return HttpResponse('2')

def group_modify(request):
	if request.method == "POST":
		group_id = request.POST['group_id']
		group_name = request.POST['group_name']
		group_members = request.POST['members']
		group_obj = models.ServerGroup.objects.get(servergroup_id=group_id)
		for i in group_obj.server_members.all():
			del_members_obj = models.ServerList.objects.filter(server_id=i.server_id)
			group_obj.server_members.remove(*del_members_obj)
		if group_members =="":
			# group_obj.update(server_members="")
			return HttpResponse('该用户下属服务器已为空值')
		else:
			members_list = group_members.split(";")
			# group_obj = models.ServerGroup.objects.get(servergroup_id=group_id)
			for i in range(len(members_list)):
				members_obj = models.ServerList.objects.filter(server_name=members_list[i])
				group_obj.server_members.add(*members_obj)

			return HttpResponse('1')
		# try:
		# 	group_obj = models.ServerGroup.objects.update(servergroup_id=group_id,servergroup_name=group_name,server_members=group_members)
		# 	group_obj.save()
		# 	return HttpResponse('1')
		# except Exception, e:
		# 	return HttpResponse(e)
		# else:
		# 	return HttpResponse('0')

def group_del(request):
	if request.method == "POST":
		group_id = request.POST['group_del']
		if group_id =="":
			return HttpResponse('未选择需要删除的用户组')
		group_list = group_id.split(";")
		for i in range(len(group_list)):
			models.ServerGroup.objects.filter(servergroup_id=group_list[i].split("|")[0]).delete()
		return HttpResponse("1")

def server_add(request):
	if request.method == "POST":
		server_name = request.POST['server_name']
		server_ip = request.POST['server_ip']
		server_memo = request.POST['server_memo']
		server_name_obj = models.ServerList.objects.filter(server_name=server_name)
		try:
			if server_name_obj:
				return HttpResponse('0')
			else:
				models.ServerList.objects.create(server_name=server_name,server_ip=server_ip,server_memo=server_memo)
		except Exception, e:
			pass
		else:
			return HttpResponse('1')
			
		return HttpResponse(server_name+server_ip+server_memo)

def server_modify(request):
	if request.method == "POST":
		server_name = request.POST['server_name']
		server_ip = request.POST['server_ip']
		server_memo = request.POST['server_memo']

		server_name_obj = models.ServerList.objects.filter(server_name=server_name)
		
		try:
			server_name_obj.update(server_name=server_name,server_ip=server_ip,server_memo=server_memo)
			return HttpResponse('1')
		except Exception, e:
			pass
		else:
			return HttpResponse('0')

def server_del(request):
	if request.method == "POST":
		server_id = request.POST['server_del']
		if server_id =="":
			return HttpResponse('未选择需要删除的服务器')
		server_list = server_id.split(";")
		for i in range(len(server_list)):
			models.ServerList.objects.filter(server_name=server_list[i].split("|")[0]).delete()
		return HttpResponse("1")


		# return HttpResponse(server_id)


def get_serverlist_for_select(request):
	'''
	主要根据id来判断，如果id存在，取出下属服务器，取出总服务器-下属服务器
	如果id不存在，则为新增，下属服务器为空
	'''
	if request.method == 'POST':
		id = request.POST['group_id']
		#多对多正向查询某个id下面有几个下属的服务器
		group_obj = models.ServerGroup.objects.get(servergroup_id=id)
		members_obj =group_obj.server_members.all().values()

		server_obj = models.ServerList.objects.all().values()
		data="{\"members_obj\":"+json.dumps(list(members_obj))+",\"all_server_obj\":"+json.dumps(list(server_obj))+"}"
		return HttpResponse(data)

def get_all_groups_list(request):
	servergroup_obj = models.ServerGroup.objects.all().values()
	data="{\"servergroup_obj\":"+json.dumps(list(servergroup_obj))+"}"
	return HttpResponse(data)

def get_all_server_list(request):
	serveruser_obj = models.ServerList.objects.all().values()
	data="{\"serveruser_obj\":"+json.dumps(list(serveruser_obj))+"}"
	return HttpResponse(data)

def saltHander(request):
	if request.method == "POST":
		'''
		加入审计处理 
		获取用户传输过来的内容,字典对象,包含用户名、IP、所用浏览器、命令执行时间、对那些服务器和服务器组进行了什么指令的操作
		'''
		cmd_user = request.user.first_name
		groupselect = request.POST['groupselect']
		userselect = request.POST['userselect']
		pars = request.POST['cmd']
		user_ip = request.META['REMOTE_ADDR']
		curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')
		#str to unicode
		#curr_date_str.decode("utf-8")
		
		#此时得到的userlist ='server_id|server_ip;server_id|server_ip;'类似的字符串
		# user_str = userselect.split(";")
		# user_list =[]
		# for i in range(len(user_str)):
			# user_list.append(user_str[i].split("|")[0])

		#断点测试
		# return HttpResponse(groupselect.encode("utf-8"))
		aa = ""
		if groupselect =="":
			pass
		else:
			group_str = groupselect.encode("utf-8").split(";")
			for index in range(len(group_str)-1):
				# group_id=group_list[i].split("|")[0]
				# return HttpResponse(str(group_str[index].split("|")[0]))
				ser_obj = models.ServerGroup.objects.get(servergroup_id=str(group_str[index].split("|")[0]))
				# return HttpResponse(ser_obj.server_members.all())
				for members in ser_obj.server_members.all():
					# return HttpResponse(members.server_id)
					aa+=str(members.server_id+"|group_members;")


		userselect+=unicode(aa,"utf-8")
		ret = rpyc_run(userselect,pars)
		logHandle.SSHLogRecord(groupselect,userselect,cmd_user,pars,user_ip)
		# data="{\"rows\":"+json.dumps(ret)+"}"
		data="{\"rows\":"+str(ret)+"}"
		#ret得到一个字典，直接返回
		return HttpResponse(ret)

def ServerSync(request):
	if request.method == "POST":
		#接收字典
		ret = rpyc_server()
		# aa=""
		# for k in dict(ret):
		# 	aa+=k

		# # data="{\"ServerInfo\":"+ret+"}"
		# # return HttpResponse(ret)
		return HttpResponse(ret)


def buildfile(request):
	ret = FileHandle.BulidNewExcel('/var/www/html/dtop/download/file/excel/')
	return HttpResponse(ret)


def download(request):
	ret = FileHandle.BulidNewExcel('/var/www/html/dtop/download/file/excel/')
	from django.http import StreamingHttpResponse
	def file_iterator(file_name,chunk_size=512):
		with open(file_name) as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break

	the_file_name ='New-'+ret+'.xls'
	response = StreamingHttpResponse(file_iterator('/var/www/html/dtop/download/file/excel/New-'+ret+'.xls'))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

	return response


# def download(request,offset):
# 	return HttpResponse('1')
