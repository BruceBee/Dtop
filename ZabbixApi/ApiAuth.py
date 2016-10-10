#coding=utf-8
import json
import urllib2
# based url and required header
url = "http://106.75.141.65:8080/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
# auth user and password
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
# except URLError as e:
    # print "Auth Failed, Please Check Your Name And Password:",e.code
except Exception as e:
    print "Auth Failed, Please Check Your Name And Password:",e.code
else:
    response = json.loads(result.read())
    result.close()
    print "Auth Successful. The Auth ID Is:",response['result']
