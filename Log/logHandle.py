#coding=utf-8
from django.shortcuts import render,HttpResponse
from Log import models
# Create your views here.
import time,datetime


def ActionRecord(user_id='-',user_name='-',act_module='-',act_type='-',act_time='-',act_detail='-'):

	act_time = time.strftime('%Y-%m-%d %H:%M:%S')

	models.ActionLog.objects.create(
		user_id=user_id,
		user_name=user_name,
		act_module=act_module,
		act_type=act_type,
		act_time=act_time,
		act_detail=act_detail
		)
	return True

def SSHLogRecord(cmd_server_group_id,cmd_server_server_id,cmd_user,cmd_command,client_ip):
	cmd_time = time.strftime('%Y-%m-%d %H:%M:%S')
	models.SSHLog.objects.create(cmd_server_group_id=cmd_server_group_id,
		cmd_server_server_id=cmd_server_server_id,
		cmd_time=cmd_time,
		cmd_user=cmd_user,
		cmd_command=cmd_command,
		client_ip=client_ip
		)
	return True


def test():

	return 22222222222