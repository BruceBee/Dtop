#coding=utf-8
import os,django,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtop.settings")# project_name 项目名称
django.setup()
import json,sys,os,django
import urllib2,datetime,time
import redis
import threading


BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from Matrix import models

def sayhai(id):
	print "告警",id
	time.sleep(5)



def redis_check(aa,bb):
	if bb == []:pass
	else:
		for j in range(3):
			# for i in range(len(bb)):
			# 	while int(aa.get(bb[i])) < 3:
			# 		print bb[i],aa.get(bb[i])
			# 		aa.incr(bb[i])
			time.sleep(5)
			print '这是第%d次告警,您有%s条告警信息' %(j+1,len(bb))



if __name__ == '__main__':

	while True:
		aa = redis.Redis(host='localhost',port=6379)
		curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串
		curr_date = datetime.datetime.strptime(curr_date_str,'%Y-%m-%d %H:%M:%S')#将当前时间转换成可加减的日期格式
		one_hour_before = curr_date + datetime.timedelta(hours=-1)
		one_hour_before_str = one_hour_before.strftime('%Y-%m-%d %H:%M:%S')
		bb = []
		for i in aa.keys():
			try:
				eventid,alertime,alertstatus= i.split("_")[1],i.split("_")[0],i.split("_")[2]
				if alertstatus == 'PROBLEM' and alertime > one_hour_before_str:
					aa.set(eventid,0)
					bb.append(eventid)
			except:
				pass 
			else:
				pass
		# print bb
		# threads = []
		# aaa=[1,2,3,4,5,6,7,8]
		# for i in range(len(aaa)):
		# 	t1 =threading.Thread(target=sayhai,args=(aaa[i],))
		# 	threads.append(t1)
		redis_check(aa,bb)

		# for t in threads:
		# 	t.start()
		time.sleep(30)







