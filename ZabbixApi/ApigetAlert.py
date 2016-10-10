#!/usr/bin/env python2.7
#coding=utf-8
import json
import urllib2,datetime,time
#xiaorui.cc
url = "http://106.75.141.65:8080/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json"}


# request json
data = json.dumps(
{
    "jsonrpc":"2.0",
    "method":"alert.get",
    "params":{
        # "output":["eventid","message",'sendto','status'],
        "output":"extend",
        "time_from":"1470439581",
        "time_till":"1470449693",
        # "filter":{"host":""},
        # "actionids":"2"
    },
    "auth":"8f810635e9ab66d66a1ca0d9e7b1f914",
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
    elif hasattr(e, 'code'):
        print 'The server could not fulfill the request.'
        print 'Error code: ', e.code
else:
    response = json.loads(result.read())
    result.close()
    print "Number Of Hosts: ", len(response['result'])
    for host in response['result']:
        alerttime = host['clock']
        print "subject:",host['subject'],"message:",host['message'],"收件人",host['sendto'],"时间",alerttime