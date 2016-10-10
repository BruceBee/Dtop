#coding=utf-8
import os,django,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtop.settings")# project_name 项目名称
django.setup()
import json,sys,os,django
import urllib2,datetime,time
import redis


BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from Matrix import models

def redisAuth():
	aa = redis.Redis(host='localhost',port=6379)
	# bb=[chr(i) for i in range(97,123)]
	for i in range(10):
		aa.set(i,'OK')

def redis_add(eventid,data):
	redis_obj = redis.Redis(host='localhost',port=6379)
	redis_obj.set(eventid,data)

def GetZabbixAlertList(url,tocken,time_from,time_till):
	data = json.dumps(
	{
	    "jsonrpc":"2.0",
	    "method":"alert.get",
	    "params":{
	        "output":"extend",
	        "time_from":time_from,
	        "time_till":time_till,
	        # "eventids":796751,
	    },
	    "auth":tocken,
	    "id":1,
	})
	# create request object
	request = urllib2.Request(url,data)
	for key in header:
	    request.add_header(key,header[key])
	# get host list
	try:
	    result = urllib2.urlopen(request)
	except URLError as e:
	    if hasattr(e, 'reason'):
	        print 'We failed to reach a server.'
	        print 'Reason: ', e.reason
	        return e.reason
	    elif hasattr(e, 'code'):
	        print 'The server could not fulfill the request.'
	        print 'Error code: ', e.code
	        return e.code

	else:
	    response = json.loads(result.read())
	    result.close()
	    # print "Number Of Hosts: ", len(response['result'])
	    # hostlist = []
	    # for host in response['result']:
	        # print "subject:",host['subject'],"message:",host['message'],"收件人",host['sendto'],"时间",host['clock']
	        # hostlist.append(host['subject'])
	    return response['result']



if __name__ == '__main__':
	# redisAuth()
	redis_add('2016-08-24 16:55:58_840733_OK','OK: Free_disk_space_is_less_than_10%_on_volume_/')
	redis_add('2016-08-24 16:44:58_840731_PROBLEM','PROBLEM: Free_disk_space_is_less_than_10%_on_volume_/')
	redis_add('2016-08-24 16:45:58_840732_PROBLEM','PROBLEM: Free_disk_space_is_less_than_10%_on_volume_/')
	# redis_add('2016-08-24 04:38:58_840664_OK','OK: Free_disk_space_is_less_than_10%_on_volume_/')
	# redis_add('2016-08-24 05:38:58_840665_PROBLEM','PROBLEM: Free_disk_space_is_less_than_10%_on_volume_/')
	# redis_add('2016-08-24 06:38:58_850666_OK','OK: Free_disk_space_is_less_than_10%_on_volume_/')





