#coding=utf-8
import os,django,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtop.settings")# project_name 项目名称
django.setup()
import json,sys,os,django
import urllib2,datetime,time
import redis

# os.environ['DJANGO_SETTINGS_MODULE'] = 'dtop.settings'
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print BASE_DIR
sys.path.append(BASE_DIR)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'dtop.settings'
from Matrix import models
# os.environ['DJANGO_SETTINGS_MODULE'] = 'dtop.settings'
# django.setup()

def ApiAuth(url):

	data = json.dumps(
	{
	    "jsonrpc": "2.0",
	    "method": "user.login",
	    "params": {
	    "user": "Admin",
	    "password": "Dt3c4ec405"
	},
	"id": 1,
	})

	# create request object
	request = urllib2.Request(url,data)
	for key in header:
	    request.add_header(key,header[key])
	# auth and get authid
	try:
	    result = urllib2.urlopen(request)
	except Exception as e:
	    print "Auth Failed, Please Check Your Name And Password:",e.code
	    return e.code
	else:
	    response = json.loads(result.read())
	    result.close()
	    # print "Auth Successful. The Auth ID Is:",response['result']
	return response['result']


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


def redis_add(eventid,subject,alerttime,status):
	redis_obj = redis.Redis(host='localhost',port=6379)
	data_k = alerttime+'_'+status+'_'+eventid
	data_v = subject
	redis_obj.set(data_k,data_v)

if __name__ == '__main__':

	url = "http://106.75.141.65:8080/zabbix/api_jsonrpc.php"
	header = {"Content-Type": "application/json"}
	currtime = time.time()
	halfhourago= ((datetime.datetime.now()-datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"))
	halfhourTime = time.mktime(time.strptime(halfhourago,'%Y-%m-%d %H:%M:%S'))

	AuthTocken = ApiAuth(url)
	AlertmessageList = GetZabbixAlertList(url,AuthTocken,halfhourTime,currtime)
	#获取当前时间
	#time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

	# alertobject = models.ZabbixAlertInfo.object.create()

	for alertobj in AlertmessageList:
		alertdict ={
			"eventid":alertobj['eventid'],
			"alerttime":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(alertobj['clock']))),
			"subject":alertobj['subject'],
			"message":alertobj['message'],
			"sendto":alertobj['sendto'],
			# "sendto":alertobj['alertid']+','+alertobj['actionid']+','+alertobj['userid'],
			"status":alertobj['subject'].split(":")[0],
		}
		#如果事件ID、告警时间以及告警主体都一样，则认定为同一条告警信息
		ZabbixAlertUpdate = models.ZabbixAlertInfo.objects.filter(eventid=alertobj['eventid'])
		if ZabbixAlertUpdate:pass
		else:models.ZabbixAlertInfo.objects.create(**alertdict)



		# redis_add(alertdict['eventid'],alertdict['subject'],alertdict['alerttime'],alertdict['status'])

		# models.ZabbixAlertInfo.objects.create(**alertdict)
		# print 'event ID:',alertobj['eventid'],'主题',alertobj['subject'],"报警详情:",alertobj['message'],'时间:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(alertobj['clock']))),\
		# '主题',alertobj['subject'],"报警详情:",alertobj['message'],"收件人",alertobj['sendto'],

		# print i['message']




